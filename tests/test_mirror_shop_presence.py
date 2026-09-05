from __future__ import annotations

from pathlib import Path

import pytest
import win32con

from tasks.mirror.shop_presence import resolve_mirror_shop_presence


def test_logged_map_hud_coins_are_not_a_shop() -> None:
    result = resolve_mirror_shop_presence(
        ["正在探索第1层", "身无分文的赌徒"],
        shop_coins=0.96,
        legend=0.777,
    )

    assert result.state == "map"
    assert result.reason in {"map_ocr", "map_legend"}


def test_legend_score_alone_is_map_even_without_ocr() -> None:
    result = resolve_mirror_shop_presence([], legend=0.777)

    assert result.state == "map"
    assert result.reason == "map_legend"


def test_legend_below_map_threshold_without_shop_controls_is_unknown() -> None:
    result = resolve_mirror_shop_presence([], legend=0.74)

    assert result.state == "unknown"


def test_shop_coins_plus_leave_without_map_evidence_is_shop() -> None:
    result = resolve_mirror_shop_presence(
        [],
        shop_coins=0.96,
        leave=0.85,
    )

    assert result.state == "shop"


def test_shop_coins_alone_is_unknown() -> None:
    result = resolve_mirror_shop_presence([], shop_coins=0.96)

    assert result.state == "unknown"


def test_map_ocr_vetoes_shop_controls() -> None:
    result = resolve_mirror_shop_presence(
        ["正在探索第1层"],
        shop_coins=0.96,
        leave=0.85,
        heal=0.9,
    )

    assert result.state == "map"
    assert result.reason == "map_ocr"


SHOP_COINS = "mirror/shop/shop_coins_assets.png"
LEGEND = "mirror/road_in_mir/legend_assets.png"
LEAVE = "mirror/shop/leave_assets.png"
HEAL = "mirror/shop/heal_sinner/heal_sinner_assets.png"
SHOP_RETURN = "mirror/shop/return_assets.png"


class FakeShopAuto:
    def __init__(self, texts: list[str], scores: dict[str, float | None]) -> None:
        self.texts = texts
        self.scores = scores

    def get_ocr_entries(self) -> list[tuple[str, tuple[int, int, int, int]]]:
        return [(text, (0, 0, 1, 1)) for text in self.texts]

    def get_image_match_score(self, target: str, model=None) -> float | None:
        return self.scores.get(target)


def test_inspect_logged_map_hud_does_not_confirm_shop() -> None:
    from tasks.mirror.shop_presence import inspect_mirror_shop_presence

    auto = FakeShopAuto(
        ["正在探索第1层"],
        {SHOP_COINS: 0.96, LEGEND: 0.777, LEAVE: 0.2, HEAL: 0.3, SHOP_RETURN: 0.1},
    )

    result = inspect_mirror_shop_presence(auto)
    assert result.state == "map"
    assert result.state != "shop"


def test_inspect_true_shop_is_confirmed() -> None:
    from tasks.mirror.shop_presence import inspect_mirror_shop_presence

    auto = FakeShopAuto(
        [],
        {SHOP_COINS: 0.96, LEGEND: 0.2, LEAVE: 0.85, HEAL: 0.3, SHOP_RETURN: 0.1},
    )

    assert inspect_mirror_shop_presence(auto).state == "shop"


def test_leave_loop_ends_on_map_without_restart() -> None:
    from tasks.mirror.shop_presence import inspect_mirror_shop_presence, should_end_shop_leave

    auto = FakeShopAuto(["正在探索第1层"], {SHOP_COINS: 0.96, LEGEND: 0.777})
    presence = inspect_mirror_shop_presence(auto)
    assert should_end_shop_leave(presence) is True


def test_three_shop_coins_sites_share_inspect_helper() -> None:
    source = Path("tasks/mirror/mirror.py").read_text(encoding="utf-8")
    assert source.count("inspect_mirror_shop_presence") >= 3
    assert 'if auto.find_element("mirror/shop/shop_coins_assets.png")' not in source
    assert 'if auto.find_element("mirror/shop/shop_coins_assets.png", model="normal")' not in source


def test_leave_loop_uses_shared_map_presence() -> None:
    source = Path("tasks/mirror/in_shop.py").read_text(encoding="utf-8")
    assert "inspect_mirror_shop_presence" in source
    assert "should_end_shop_leave" in source


def test_is_on_mirror_map_logged_hud() -> None:
    from tasks.mirror.shop_presence import is_on_mirror_map

    auto = FakeShopAuto(
        ["正在探索第1层"],
        {SHOP_COINS: 0.96, LEGEND: 0.777, LEAVE: 0.2, HEAL: 0.3, SHOP_RETURN: 0.1},
    )
    assert is_on_mirror_map(auto) is True
    assert is_on_mirror_map(auto, use_ocr=False) is True


def test_is_on_mirror_map_rejects_true_shop() -> None:
    from tasks.mirror.shop_presence import is_on_mirror_map

    auto = FakeShopAuto(
        [],
        {SHOP_COINS: 0.96, LEGEND: 0.2, LEAVE: 0.85, HEAL: 0.3, SHOP_RETURN: 0.1},
    )
    assert is_on_mirror_map(auto) is False


def test_is_on_mirror_map_ocr_fallback_without_legend() -> None:
    from tasks.mirror.shop_presence import is_on_mirror_map

    auto = FakeShopAuto(["正在探索第1层"], {LEGEND: 0.2})
    assert is_on_mirror_map(auto) is True
    assert is_on_mirror_map(auto, use_ocr=False) is False


def test_is_on_mirror_map_missing_score_api_is_not_map() -> None:
    from tasks.mirror.shop_presence import is_on_mirror_map

    class IncompleteAuto:
        pass

    assert is_on_mirror_map(IncompleteAuto(), use_ocr=False) is False


def test_pathfinding_gates_do_not_use_default_legend_threshold() -> None:
    for path in (
        "tasks/mirror/mirror.py",
        "tasks/mirror/reward_card.py",
        "tasks/mirror/select_theme_pack.py",
        "tasks/battle/battle.py",
        "tasks/base/back_init_menu.py",
    ):
        source = Path(path).read_text(encoding="utf-8")
        assert "is_on_mirror_map" in source
        assert 'find_element("mirror/road_in_mir/legend_assets.png"' not in source


def test_search_road_does_not_skip_farthest_on_background_click() -> None:
    source = Path("tasks/mirror/mirror.py").read_text(encoding="utf-8")
    start = source.index("def search_road(self):")
    end = source.index("def ", start + 1)
    search_road = source[start:end]
    assert "if cfg.background_click:" not in search_road
    assert "search_road_farthest_distance()" in search_road


def test_farthest_returns_false_when_scroll_unavailable(monkeypatch) -> None:
    import tasks.mirror.search_road as search_road
    from module.my_error.my_error import InputAttributeError

    monkeypatch.setattr(search_road.auto, "mouse_click_blank", lambda: None)
    monkeypatch.setattr(search_road.auto, "mouse_scroll", lambda: False)

    try:
        assert search_road.search_road_farthest_distance() is False
    except InputAttributeError:
        pytest.fail("滚轮失败必须返回 False，不能抛 InputAttributeError")


def test_background_mouse_scroll_sends_wheel_message(monkeypatch) -> None:
    from module.automation.input_handlers.input import BackgroundInput

    messages: list[tuple[int, int, int]] = []

    class FakeHandle:
        hwnd = 123
        isMinimized = False

        def rect(self, _client: bool = True):
            return (0, 0, 1600, 900)

    class FakeScreen:
        handle = FakeHandle()

    monkeypatch.setattr(
        "module.automation.input_handlers.input.screen",
        FakeScreen(),
    )
    monkeypatch.setattr(
        "module.automation.input_handlers.input.win32api.PostMessage",
        lambda hwnd, msg, wparam, lparam: messages.append((hwnd, msg, wparam)),
    )
    monkeypatch.setattr(
        "module.automation.input_handlers.input.win32gui.SendMessage",
        lambda hwnd, msg, wparam, lparam: messages.append((hwnd, msg, wparam)),
    )
    monkeypatch.setattr(
        BackgroundInput,
        "set_active",
        lambda self: None,
    )
    monkeypatch.setattr(
        BackgroundInput,
        "wait_pause",
        lambda self: None,
    )

    handler = BackgroundInput()
    handler.use_post_message = True
    assert handler.mouse_scroll(-3) is True
    assert any(msg == win32con.WM_MOUSEWHEEL for _, msg, _ in messages)
