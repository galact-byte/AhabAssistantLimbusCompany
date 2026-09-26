"""以可变列表画面驱动真实选队流程；不连接游戏或发送系统输入。"""
import importlib
from types import SimpleNamespace

import pytest
from PIL import Image

formation = importlib.import_module("tasks.teams.team_formation")


class ListScreen:
    def __init__(self, names=None, start=0):
        self.names = names or ["剧情关卡", "编队#3", "自定义队伍"] + [f"编队#{i}" for i in range(4, 41)]
        self.start = start
        self.step = 1
        self.selected = "未选中"
        self.screenshot = Image.new("RGB", (1600, 900))
        self.frames = 0
        self.scrolls = []
        self.clicks = []
        self.wrong_clicks = 0
        self.stuck = False
        self.empty = False
        self.missing_frame = False
        self.saved = []

    def take_screenshot(self):
        self.frames += 1
        assert self.frames < 600, "截图失败不能无限循环"
        return None if self.missing_frame else self.screenshot

    def find_element(self, target, **kwargs):
        return (1500, 222) if target == "teams/identify_assets.png" else None

    def click_element(self, *args, **kwargs):
        return False

    def get_ocr_entries(self):
        if self.empty:
            return []
        entries = [("编队", (125, 345, 180, 367)), ("预设#1", (100, 180, 190, 205)),
                   (self.selected, (400, 40, 600, 70))]
        whole = int(self.start)
        for i, name in enumerate(self.names[whole:whole + 9]):
            y = 400 + (i - (self.start - whole)) * 45
            if 390 <= y <= 727:
                entries.append((name, (100, y - 10, 205, y + 10)))
        return entries

    def get_text_positions(self, **kwargs):
        return {text: [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2] for text, b in self.get_ocr_entries()}

    def mouse_click(self, x, y, **kwargs):
        if x < 250 and y >= 377:
            index = min(round(self.start + (y - 400) / 45), len(self.names) - 1)
            self.clicks.append(index)
            if self.wrong_clicks:
                self.wrong_clicks -= 1
                self.selected = self.names[min(index + 1, len(self.names) - 1)]
            else:
                self.selected = self.names[index]
        return True

    def mouse_action_with_pos(self, pos, **kwargs):
        return self.mouse_click(*pos)

    def mouse_swipe_for_team_scroll(self, x, y, dy=0, **kwargs):
        self.scrolls.append(dy)
        if not self.stuck:
            self.start = max(0, min(len(self.names) - 8, self.start + (-self.step if dy > 0 else self.step)))
        return True


@pytest.fixture
def screen(monkeypatch, tmp_path):
    fake = ListScreen()
    monkeypatch.setattr(formation, "auto", fake)
    monkeypatch.setattr(formation, "sleep", lambda *_: None)
    monkeypatch.setattr(formation, "cfg", SimpleNamespace(set_win_size=900, select_team_by_order=True, simulator=False))
    monkeypatch.chdir(tmp_path)
    return fake


def test_recorded_900p_top_rows_select_without_unresponsive_wheel(screen, monkeypatch):
    # 2026-09-26 04:04 失败帧：顶部“剧情关卡”及“编队#2”，滚轮消息不改变列表。
    screen.names = ["剧情关卡", "编队#2", "编队#3", "编队#4", "编队#5", "编队#6", "编队#7"]
    screen.stuck = True
    original_entries = screen.get_ocr_entries

    def captured_entries():
        entries = original_entries()
        entries[0] = ("编队", (140, 344, 184, 371))
        for index, name in enumerate(screen.names):
            if name == "剧情关卡":
                entries[index + 3] = (name, (130, 377, 199, 402))
            else:
                y = 422 + (index - 1) * 45
                entries[index + 3] = (name, (132, y, 195, y + 25))
        return entries

    monkeypatch.setattr(screen, "get_ocr_entries", captured_entries)
    for target in (1, 2):
        screen.frames = 0
        assert formation.select_battle_team(target) is True
        assert screen.selected == screen.names[target - 1]
    assert screen.clicks == [0, 1]
    assert screen.scrolls == []


def test_top_geometry_without_known_first_item_cannot_authorize_ordered_click(screen):
    screen.names[0] = "未知首项"
    screen.stuck = True
    assert formation.select_battle_team(2) is False
    assert not screen.clicks


def test_order_uses_current_second_item_not_number_two_and_corrects_wrong_click(screen):
    screen.start = 16
    screen.wrong_clicks = 1
    assert formation.select_battle_team(2) is True
    assert screen.selected == "编队#3"
    assert screen.clicks[-2:] == [1, 1]


@pytest.mark.parametrize("target", [1, 3, 8, 35, 40])
def test_custom_names_and_last_of_40_teams(screen, target):
    assert formation.select_battle_team(target) is True
    assert screen.selected == screen.names[target - 1]


@pytest.mark.parametrize("step", [0.5, 3, 5])
def test_observed_displacement_not_assumed_wheel_pixel_distance(screen, step):
    screen.step = step
    assert formation.select_battle_team(35) is True
    assert screen.selected == "编队#35"


def test_repeated_selection_resets_current_scroll_position(screen):
    for target in [40, 2, 35, 1]:
        screen.frames = 0
        assert formation.select_battle_team(target) is True
        assert screen.selected == screen.names[target - 1]


def test_number_mode_finds_reordered_two_not_twenty_or_preset(screen, monkeypatch):
    monkeypatch.setattr(formation.cfg, "select_team_by_order", False)
    screen.names[20] = "编队#2"
    assert formation.select_battle_team(2) is True
    assert screen.selected == "编队#2"
    assert screen.clicks[-1] == 20


@pytest.mark.parametrize("failure", ["empty", "missing_frame", "stuck", "wrong_clicks", "duplicate", "absent"])
def test_uncertain_selection_fails_with_finite_budget(screen, failure):
    if failure == "duplicate":
        screen.names[1] = screen.names[2]
    elif failure == "absent":
        screen.names = screen.names[:8]
    elif failure == "stuck":
        screen.start = 16
        screen.stuck = True
    elif failure == "wrong_clicks":
        screen.wrong_clicks = 100
    else:
        setattr(screen, failure, True)
    assert formation.select_battle_team(40 if failure == "absent" else 2) is False
    assert screen.frames < 600


def test_temporary_screenshot_failure_recovers_without_using_stale_frame(screen, monkeypatch):
    original = screen.take_screenshot
    calls = []

    def capture():
        calls.append(1)
        return None if len(calls) <= 2 else original()

    monkeypatch.setattr(screen, "take_screenshot", capture)
    assert formation.select_battle_team(2) is True
    assert len(calls) > 2


def test_home_prompt_is_closed_before_reading_team_list(screen, monkeypatch):
    open_prompt = [True]
    original_find = screen.find_element

    def find(target, **kwargs):
        if target in ("home/first_prompt_assets.png", "home/back_assets.png"):
            return (1, 1) if open_prompt[0] else None
        return None if open_prompt[0] else original_find(target, **kwargs)

    def click(target, **kwargs):
        assert target == "home/back_assets.png"
        open_prompt[0] = False
        return True

    monkeypatch.setattr(screen, "find_element", find)
    monkeypatch.setattr(screen, "click_element", click)
    assert formation.select_battle_team(2) is True


def test_ocr_exception_reports_failure_instead_of_escaping(screen, monkeypatch):
    def broken_ocr():
        raise RuntimeError("OCR unavailable")
    monkeypatch.setattr(screen, "get_ocr_entries", broken_ocr)
    assert formation.select_battle_team(2) is False


def test_ordered_selection_does_not_scan_unrelated_distant_duplicate(screen):
    screen.names[-1] = screen.names[1]
    assert formation.select_battle_team(2) is True
    assert screen.clicks == [1]
    assert len(screen.scrolls) <= 8


@pytest.mark.parametrize("count", [12, 40])
def test_second_slot_does_not_require_full_list_scan(screen, count):
    screen.names = screen.names[:count]
    assert formation.select_battle_team(2) is True
    assert screen.selected == "编队#3"
    assert len(screen.scrolls) <= 8


def test_named_visible_target_does_not_require_reset_or_40_slots(screen, monkeypatch):
    monkeypatch.setattr(formation.cfg, "select_team_by_order", False)
    screen.names = ["编队#2", "编队#20", "编队#3"]
    screen.stuck = True
    assert formation.select_battle_team(2) is True
    assert screen.selected == "编队#2"
    assert not screen.scrolls


def test_scroll_stopping_mid_list_cannot_masquerade_as_top(screen, monkeypatch):
    screen.start = 16
    original = screen.mouse_swipe_for_team_scroll

    def blocked_above_midpoint(x, y, dy=0, **kwargs):
        result = original(x, y, dy=dy, **kwargs)
        screen.start = max(16, screen.start)
        return result

    monkeypatch.setattr(screen, "mouse_swipe_for_team_scroll", blocked_above_midpoint)
    assert formation.select_battle_team(2) is False
    assert not screen.clicks


def test_upward_scroll_failure_mid_list_cannot_authorize_ordered_selection(screen, monkeypatch):
    screen.start = 16
    original = screen.mouse_swipe_for_team_scroll

    def only_down(x, y, dy=0, **kwargs):
        if dy > 0:
            screen.scrolls.append(dy)
            return True
        return original(x, y, dy=dy, **kwargs)

    monkeypatch.setattr(screen, "mouse_swipe_for_team_scroll", only_down)
    assert formation.select_battle_team(2) is False
    assert not screen.clicks


def test_failure_saves_available_frame(screen, tmp_path):
    screen.empty = True
    assert formation.select_battle_team(2) is False
    screenshots = list((tmp_path / "logs").glob("team-selection-failed-*.png"))
    assert len(screenshots) == 1
    assert Image.open(screenshots[0]).size == (1600, 900)


@pytest.mark.parametrize("simulator_type", [0, 10])
def test_simulator_keeps_specialized_gesture_path(screen, monkeypatch, simulator_type):
    monkeypatch.setattr(formation.cfg, "simulator", True)
    monkeypatch.setattr(formation.cfg, "simulator_type", simulator_type, raising=False)
    assert formation.select_battle_team(2) is True
    assert all(abs(distance) > 100 for distance in screen.scrolls)


@pytest.mark.parametrize("retry_ok", [True, False])
def test_mirror_team_confirmation_failure_is_terminal(monkeypatch, retry_ok):
    mirror = importlib.import_module("tasks.mirror.mirror")
    calls = []
    monkeypatch.setattr(mirror, "select_battle_team", lambda n: True)
    monkeypatch.setattr(mirror, "cfg", SimpleNamespace(config=SimpleNamespace(teams={})))
    monkeypatch.setattr(mirror, "auto", SimpleNamespace(
        model="clam", find_element=lambda *a, **k: None,
        take_screenshot=lambda: object(), click_element=lambda *a, **k: False,
        find_language_text=lambda *a, **k: False, mouse_to_blank=lambda **k: None,
    ))
    monkeypatch.setattr(mirror, "retry", lambda: retry_ok)
    monkeypatch.setattr(mirror, "back_init_menu", lambda: calls.append("home") or True)
    monkeypatch.setattr(mirror, "sleep", lambda *_: None)
    monkeypatch.setattr(mirror.time, "sleep", lambda *_: None)
    with pytest.raises(mirror.cannotOperateGameError):
        mirror.Mirror.select_mirror_team(SimpleNamespace(team_number=2, team_order=2))
    assert calls == (["home"] if retry_ok else [])


def test_mirror_team_confirmation_reaches_coins(monkeypatch):
    mirror = importlib.import_module("tasks.mirror.mirror")
    calls = []
    monkeypatch.setattr(mirror, "select_battle_team", lambda n: True)
    monkeypatch.setattr(mirror, "cfg", SimpleNamespace(config=SimpleNamespace(teams={})))
    monkeypatch.setattr(mirror, "auto", SimpleNamespace(
        model="clam",
        find_element=lambda path, **kwargs: (1, 1) if calls and path.endswith("coins_assets.png") else None,
        take_screenshot=lambda: object(),
        click_element=lambda path: calls.append(path) or True,
        mouse_to_blank=lambda **kwargs: None,
    ))
    monkeypatch.setattr(mirror, "retry", lambda: True)
    monkeypatch.setattr(mirror, "sleep", lambda *_: None)
    monkeypatch.setattr(mirror.time, "sleep", lambda *_: None)
    mirror.Mirror.select_mirror_team(SimpleNamespace(team_number=2, team_order=2))
    assert calls == ["mirror/road_to_mir/level_confirm_assets.png"]


def test_mirror_team_confirmation_exception_stops_top_level(monkeypatch):
    scheme = importlib.import_module("tasks.base.script_task_scheme")
    mirror = importlib.import_module("tasks.mirror.mirror")
    monkeypatch.setattr(scheme.cfg, "auto_hard_mirror", False)
    def fail_confirmation():
        raise mirror.cannotOperateGameError("选队确认超时")

    monkeypatch.setattr(scheme, "Mirror", lambda *_: SimpleNamespace(run=fail_confirmation))
    monkeypatch.setattr(scheme, "back_init_menu", lambda: pytest.fail("失败后不能按成功返回首页"))
    monkeypatch.setattr(scheme, "make_enkephalin_module", lambda: pytest.fail("失败后不能按成功换饼"))
    assert scheme.onetime_mir_process(None, 2) is False


def test_mirror_failure_never_confirms_or_loads_team_code(monkeypatch):
    mirror = importlib.import_module("tasks.mirror.mirror")
    attempts = []
    monkeypatch.setattr(mirror, "select_battle_team", lambda n: attempts.append(n) or False)
    monkeypatch.setattr(mirror, "auto", SimpleNamespace(
        click_element=lambda *a, **k: pytest.fail("选队失败后不得确认")))
    monkeypatch.setattr(mirror, "load_team_code_in_game", lambda *a: pytest.fail("失败后不得加载编队码"))
    with pytest.raises(mirror.unableToFindTeamError):
        mirror.Mirror.select_mirror_team(SimpleNamespace(team_number=2, team_order=2))
    assert len(attempts) == 6
