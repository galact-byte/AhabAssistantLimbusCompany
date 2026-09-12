import importlib
from types import SimpleNamespace

import pytest


@pytest.mark.parametrize("failure", ["screenshot", "recognition"])
def test_theme_pack_failure_has_bounded_recovery(monkeypatch, failure):
    module = importlib.import_module("tasks.mirror.select_theme_pack")
    calls = []
    frames = 0

    def screenshot(*args, **kwargs):
        nonlocal frames
        frames += 1
        if frames > 40:
            pytest.fail("主题包失败超过40帧，预算被continue绕过")
        return None if failure == "screenshot" else object()

    def find(*args, **kwargs):
        raise ValueError("识别异常")

    monkeypatch.setattr(module, "auto", SimpleNamespace(take_screenshot=screenshot, find_element=find))
    monkeypatch.setattr(module, "cfg", SimpleNamespace(set_win_size=1080, select_event_pack=False, skip_event_pack=False))
    monkeypatch.setattr(module, "path_manager", SimpleNamespace(current_language="zh_cn"))
    monkeypatch.setattr(module, "theme_list", SimpleNamespace(get_effective_theme_pack_list=lambda *args: {}, preferred_thresholds=0))
    monkeypatch.setattr(module, "is_on_mirror_map", lambda _: False)
    monkeypatch.setattr(module, "back_init_menu", lambda **kwargs: calls.append(kwargs) or False)
    module.select_theme_pack(floor=1)
    assert calls == [{"allow_restart": False}]
