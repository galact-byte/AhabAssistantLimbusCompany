"""issue #893 回归：ONNX None 兜底与地图上键盘恢复，避免死点设置齿轮。"""

from __future__ import annotations

from pathlib import Path

import tasks.mirror.search_road as search_road


class _FakeAuto:
    """记录键盘/点击调用的假 auto，用于驱动纯逻辑分支。"""

    def __init__(self, *, find_return=None, click_map=None, enter_hits=()):
        self._find_return = find_return
        self._click_map = click_map or {}
        self._enter_hits = list(enter_hits)
        self.key_presses: list[str] = []
        self.click_calls: list[str] = []

    def click_element(self, target, *args, **kwargs):
        self.click_calls.append(target)
        if target == "mirror/road_in_mir/enter_assets.png":
            if self._enter_hits:
                return self._enter_hits.pop(0)
            return False
        return self._click_map.get(target, False)

    def find_element(self, *args, **kwargs):
        return self._find_return

    def take_screenshot(self, *args, **kwargs):
        return object()

    def get_restore_time(self):
        return None

    def key_press(self, key):
        self.key_presses.append(key)

    def mouse_to_blank(self):
        pass


def test_road_map_returns_empty_when_bus_missing(monkeypatch) -> None:
    """公交车定位不到时返回空路径而不是抛异常。"""
    fake = _FakeAuto(find_return=None)
    monkeypatch.setattr(search_road, "auto", fake)

    result = search_road.search_road_from_road_map()

    assert result == ([], [])


def test_road_map_returns_empty_when_onnx_none(monkeypatch) -> None:
    """ONNX identify_nodes 返回 None 时返回空路径而不是抛 TypeError。"""
    monkeypatch.setattr(search_road.cfg, "set_win_size", 1440, raising=False)
    fake = _FakeAuto(find_return=(100, 690))
    monkeypatch.setattr(search_road, "auto", fake)
    monkeypatch.setattr(search_road, "identify_nodes", lambda *_a, **_k: None)

    result = search_road.search_road_from_road_map()

    assert result == ([], [])


def test_keyboard_node_fallback_enters_node(monkeypatch) -> None:
    """键盘兜底按方向键并成功进入节点。"""
    fake = _FakeAuto(enter_hits=[False, True])
    monkeypatch.setattr(search_road, "auto", fake)

    assert search_road.keyboard_node_fallback() is True
    assert fake.key_presses  # 至少按过方向键


def test_keyboard_node_fallback_returns_false_when_stuck(monkeypatch) -> None:
    """始终进不去节点时返回 False，交回上层继续兜底。"""
    fake = _FakeAuto(enter_hits=[])
    monkeypatch.setattr(search_road, "auto", fake)

    assert search_road.keyboard_node_fallback() is False


def test_recovery_loop_prefers_keyboard_over_setting_gear() -> None:
    """search_road 恢复分支必须先用地图键盘兜底，而非死点设置齿轮。"""
    source = Path("tasks/mirror/mirror.py").read_text(encoding="utf-8")
    start = source.index("def search_road(self):")
    end = source.index("\n    def ", start + 1)
    body = source[start:end]

    assert "keyboard_node_fallback" in body
    assert "is_on_mirror_map(auto, use_ocr=False)" in body
    # 键盘兜底必须出现在设置齿轮点击之前
    assert body.index("keyboard_node_fallback") < body.index("mirror/road_in_mir/setting_assets.png")


def test_recovery_to_window_uses_sub_default_threshold() -> None:
    """issue #893 日得：回到窗口在 1600x900 实测 0.78，必须低于默认 0.8 才能点出。"""
    source = Path("tasks/mirror/mirror.py").read_text(encoding="utf-8")
    start = source.index("def search_road(self):")
    end = source.index("\n    def ", start + 1)
    body = source[start:end]

    line = next(ln for ln in body.splitlines() if "to_window_assets.png" in ln and "click_element" in ln)
    assert "threshold=0.7" in line
