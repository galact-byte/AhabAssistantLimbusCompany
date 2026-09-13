"""恢复测试只替换窗口/启动边界，不接触真实游戏。"""
import ast
import importlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from tasks.base.home_page import find_home_drive


def test_background_window_missing_does_not_launch_game(monkeypatch):
    module = importlib.import_module("module.automation.screenshot")
    game = importlib.import_module("module.game_and_screen")
    script = importlib.import_module("tasks.base.script_task_scheme")
    operations = []
    monkeypatch.setattr(module, "screen", SimpleNamespace(handle=SimpleNamespace(hwnd=0)))
    monkeypatch.setattr(game.game_process, "close_game", lambda: operations.append("close"))
    monkeypatch.setattr(script, "init_game", lambda: operations.append("launch"))
    assert module.ScreenShot.background_screenshot() is None
    assert operations == []


def test_restart_owns_close_launch_and_home_without_nested_launch(monkeypatch):
    retry = importlib.import_module("tasks.base.retry")
    script = importlib.import_module("tasks.base.script_task_scheme")
    home = importlib.import_module("tasks.base.back_init_menu")
    operations = []
    nested_results = []
    monkeypatch.setattr(retry, "kill_game", lambda: operations.append("close"))
    def launch():
        operations.append("launch")
        if len(operations) < 5:
            nested_results.append(retry.restart_game(close_first=True))
    monkeypatch.setattr(script, "init_game", launch)
    monkeypatch.setattr(home, "back_init_menu", lambda **kw: operations.append(("home", kw)) or True)
    monkeypatch.setattr(retry, "sleep", lambda _: None)
    assert retry.restart_game(close_first=True) is True
    assert operations == ["close", "launch", ("home", {"allow_restart": False})]
    assert nested_results == [False]


@pytest.mark.parametrize("failure", ["launch", "home"])
def test_failed_restart_releases_owner_for_later_attempt(monkeypatch, failure):
    retry = importlib.import_module("tasks.base.retry")
    script = importlib.import_module("tasks.base.script_task_scheme")
    home = importlib.import_module("tasks.base.back_init_menu")
    monkeypatch.setattr(retry, "kill_game", lambda: None)
    monkeypatch.setattr(retry, "sleep", lambda _: None)
    def launch():
        if failure == "launch":
            raise RuntimeError("launch failed")
    monkeypatch.setattr(script, "init_game", launch)
    monkeypatch.setattr(home, "back_init_menu", lambda **kw: False)
    with pytest.raises(Exception):
        retry.restart_game(close_first=True)
    monkeypatch.setattr(script, "init_game", lambda: None)
    monkeypatch.setattr(home, "back_init_menu", lambda **kw: True)
    assert retry.restart_game(close_first=True) is True


@pytest.mark.parametrize("raises", [False, True])
def test_business_screenshot_failure_recovers_once_outside_capture_lock(monkeypatch, raises):
    import threading

    from PIL import Image
    module = importlib.import_module("module.automation.automation")
    retry = importlib.import_module("tasks.base.retry")
    auto = object.__new__(module.Automation)
    auto.last_screenshot_time = 0
    auto._screenshot_lock = threading.Lock()
    auto._remember_screenshot = lambda _: None
    operations = []
    clock = [0.0]
    image = Image.new("RGB", (2, 2))
    captures = [0]
    def capture(_):
        captures[0] += 1
        if operations:
            return image
        if raises and captures[0] == 1:
            raise RuntimeError("capture failed")
        return None
    def recover(**kwargs):
        assert auto._screenshot_lock.acquire(blocking=False)
        auto._screenshot_lock.release()
        operations.append(kwargs)
        return True
    monkeypatch.setattr(module.ScreenShot, "take_screenshot", capture)
    monkeypatch.setattr(module.time, "monotonic", lambda: clock[0])
    monkeypatch.setattr(module.time, "sleep", lambda _: None)
    monkeypatch.setattr(retry, "restart_game", recover)
    assert auto.take_screenshot() is None
    clock[0] = 61
    assert auto.take_screenshot() is None
    assert operations == [{"close_first": True}]
    assert auto.take_screenshot() is image


@pytest.mark.parametrize("remaining, expected", [(80, "clam"), (60, "normal"), (14, "aggressive")])
def test_mirror_search_mode_survives_next_iteration(remaining, expected):
    path = Path(__file__).resolve().parents[1] / "tasks/mirror/mirror.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Mirror")
    run = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "run")
    auto = SimpleNamespace(model="clam", click_element=lambda *a, **kw: False,
                           find_element=lambda *a, **kw: False)
    def capture():
        raise StopIteration
    auto.take_screenshot = capture
    namespace = dict(auto=auto, time=SimpleNamespace(time=lambda: 0))
    exec(compile(ast.Module(body=[run], type_ignores=[]), str(path), "exec"), namespace)
    with pytest.raises(StopIteration):
        namespace["run"](SimpleNamespace(LOOP_COUNT=remaining))
    assert auto.model == expected


def test_battle_total_timeout_does_not_return_home_twice(monkeypatch):
    from test_daily_event_recovery import _FightEventAuto
    module = importlib.import_module("tasks.battle.battle")
    retry = importlib.import_module("tasks.base.retry")
    home = importlib.import_module("tasks.base.back_init_menu")
    calls = []
    monkeypatch.setattr(module, "auto", _FightEventAuto([[]]))
    monkeypatch.setattr(module, "handle_server_error_dialog", lambda: None)
    monkeypatch.setattr(retry, "check_times", lambda *a, **kw: True)
    monkeypatch.setattr(home, "back_init_menu", lambda: calls.append("home"))
    assert module.Battle(is_tool=True).fight() is False
    assert calls == []


def test_retry_missing_frames_has_terminal_deadline(monkeypatch):
    module = importlib.import_module("tasks.base.retry")
    calls = []
    frames = [0]
    def capture():
        frames[0] += 1
        if frames[0] > 4:
            raise AssertionError("截图失败不能无限绕过恢复期限")
        return None
    monkeypatch.setattr(module, "cfg", SimpleNamespace(config=SimpleNamespace(simulator=True)))
    monkeypatch.setattr(module, "auto", SimpleNamespace(take_screenshot_with_color=capture, get_restore_time=lambda: None))
    monkeypatch.setattr(module, "ensure_simulator_game_started", lambda: False)
    monkeypatch.setattr(module.time, "monotonic", lambda: frames[0] * 61)
    monkeypatch.setattr(module, "sleep", lambda _: None)
    monkeypatch.setattr(module, "restart_game", lambda **kw: calls.append(kw) or True)
    assert module.retry() is False
    assert calls == [{"close_first": True}]


def test_return_home_exhaustion_delegates_one_owned_restart(monkeypatch):
    from test_daily_event_recovery import _BackInitMenuEventAuto
    module = importlib.import_module("tasks.base.back_init_menu")
    retry = importlib.import_module("tasks.base.retry")
    operations = []
    monkeypatch.setattr(module, "auto", _BackInitMenuEventAuto([[]]))
    monkeypatch.setattr(module, "LOOP_COUNT", 0)
    monkeypatch.setattr(retry, "kill_game", lambda: operations.append("unowned close"))
    def restart(**kwargs):
        operations.append(kwargs)
        return True
    monkeypatch.setattr(retry, "restart_game", restart)
    # 旧实现忽略返回值并重进循环；第二次调用即终止测试防止无限循环。
    def sleep(_):
        raise AssertionError("确认主页后不应重走恢复循环")
    monkeypatch.setattr(module, "sleep", sleep)
    assert module.back_init_menu() is True
    assert operations == [{"close_first": True}]


@pytest.mark.parametrize("missing_frame", [False, True])
def test_mirror_reentry_exhaustion_is_explicit_failure(missing_frame):
    path = Path(__file__).resolve().parents[1] / "tasks/mirror/mirror.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "road_to_mir")
    frames = []
    def capture():
        frames.append(1)
        if len(frames) > 40:
            raise AssertionError("重进镜牢必须有界")
        return None if missing_frame else object()
    auto = SimpleNamespace(
        take_screenshot=capture, mouse_to_blank=lambda: None,
        find_element=lambda *a, **kw: False, click_element=lambda *a, **kw: False,
        find_text_element=lambda *a, **kw: True, get_ocr_entries=lambda: [],
    )
    namespace = dict(auto=auto, retry=lambda: True, sleep=lambda _: None, find_home_drive=find_home_drive,
                     inspect_mirror_shop_presence=lambda _: SimpleNamespace(state="unknown"),
                     is_on_mirror_map=lambda _: False,
                     ImageUtils=SimpleNamespace(get_bbox=lambda _: (0, 0, 10, 10), load_image=lambda _: None),
                     log=SimpleNamespace(error=lambda _: None), back_init_menu=lambda: False)
    exec(compile(ast.Module(body=[method], type_ignores=[]), str(path), "exec"), namespace)
    assert namespace["road_to_mir"](SimpleNamespace()) is False
    assert len(frames) <= 31


def test_maintenance_during_recovery_does_not_close_game_again(monkeypatch):
    from test_daily_event_recovery import _BackInitMenuEventAuto
    module = importlib.import_module("tasks.base.back_init_menu")
    retry = importlib.import_module("tasks.base.retry")
    auto = _BackInitMenuEventAuto([[]])
    operations = []
    monkeypatch.setattr(module, "auto", auto)
    monkeypatch.setattr(auto, "find_element", lambda asset, **kw: asset == "base/notification_close_assets.png")
    monkeypatch.setattr(module, "ensure_simulator_game_started", lambda: False)
    monkeypatch.setattr(module, "retry", lambda: True)
    monkeypatch.setattr(retry, "kill_game", lambda: operations.append("close"))
    assert module.back_init_menu(allow_restart=False) is False
    assert operations == []


def _mirror_class():
    # 镜牢包初始化会读取整套商店图片；沿用既有测试的AST方法加载，执行真实方法体。
    path = Path(__file__).resolve().parents[1] / "tasks/mirror/mirror.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Mirror")
    methods = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in ("_fight", "_time_call")]
    return path, methods


@pytest.mark.parametrize("landing", ["home", "home_ocr", "map", "unknown", "failed"])
def test_mirror_false_battle_recovers_by_landing_not_boolean(landing):
    path, methods = _mirror_class()
    operations = []
    auto = SimpleNamespace(
        take_screenshot=lambda: object(),
        find_element=lambda asset, **kw: landing == "home" and asset == "home/window_assets.png",
        get_ocr_entries=lambda: [("玻璃窗", (20, 800, 100, 850)), ("驾驶席", (200, 800, 280, 850))] if landing in ("home", "home_ocr") else [],
    )
    namespace = dict(
        time=SimpleNamespace(time=lambda: 0), find_home_drive=find_home_drive,
        battle=SimpleNamespace(fight=lambda **kw: False), auto=auto,
        is_on_mirror_map=lambda *a, **kw: landing == "map",
        back_init_menu=lambda **kw: operations.append("home") or landing != "failed",
        restart_game=lambda **kw: operations.append("restart") or landing != "failed",
        cannotOperateGameError=RuntimeError,
        log=SimpleNamespace(warning=lambda *a: None, debug=lambda *a: None),
    )
    exec(compile(ast.Module(body=methods, type_ignores=[]), str(path), "exec"), namespace)
    mirror = SimpleNamespace(
        avoid_skill_3=False, prioritize_skill_3=False, defense_first_round=False,
        defense_for_solo_state=None, battle_total_time=0,
        road_to_mir=lambda: operations.append("enter"),
    )
    mirror._time_call = lambda *a, **kw: namespace["_time_call"](mirror, *a, **kw)
    if landing == "failed":
        with pytest.raises(RuntimeError):
            namespace["_fight"](mirror)
        assert operations == ["home", "restart"]
        return
    namespace["_fight"](mirror)
    assert operations == {"home": ["enter"], "home_ocr": ["enter"], "map": [], "unknown": ["home", "enter"]}[landing]
