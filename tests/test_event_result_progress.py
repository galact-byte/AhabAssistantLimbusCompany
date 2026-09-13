"""结果页持续不推进必须在局部期限退出，点击命中不是页面推进。"""
import importlib

import pytest
from test_daily_event_recovery import _FightEventAuto

from tasks.event_page import resolve_event_page


@pytest.mark.parametrize("outcome", ["判定成功", "判定失败"])
def test_result_skip_requires_bottom_right_geometry(outcome):
    entries = [(outcome, (500, 200, 700, 240)), ("SKIP", (1380, 796, 1455, 824))]
    result = resolve_event_page(entries)
    assert result.state == "advance"
    assert result.position == (1417, 810)
    assert result.reason == "result_skip"


@pytest.mark.parametrize("text,bounds", [
    ("SKIP", (10, 10, 80, 40)),
    ("故事里继续前进", (680, 800, 760, 840)),
    ("继续", (680, 100, 760, 140)),
    ("SKIP", (1400, 810, 1300, 790)),
])
def test_result_does_not_click_narrative_or_misplaced_action(text, bounds):
    result = resolve_event_page([("判定成功", (500, 200, 700, 240)), (text, bounds)])
    assert result.state == "wait"
    assert result.position is None


@pytest.mark.parametrize("template", [False, True])
@pytest.mark.parametrize("button", [None, "继续", "SKIP"])
def test_stuck_result_exits_before_total_battle_timeout(monkeypatch, template, button):
    module = importlib.import_module("tasks.battle.battle")
    entries = [("判定成功", (500, 200, 700, 240))]
    if button:
        entries.append((button, (1380, 796, 1455, 824)))
    auto = _FightEventAuto([entries] * 100)
    monkeypatch.setattr(module, "auto", auto)
    monkeypatch.setattr(module, "sleep", lambda _: None)
    monkeypatch.setattr(module, "monotonic", lambda: auto._frame, raising=False)
    monkeypatch.setattr(module, "handle_server_error_dialog", lambda: None)
    monkeypatch.setattr(module, "retry", lambda: True)
    monkeypatch.setattr(auto, "click_element", lambda asset, **kw: template and auto._frame <= 100 and asset == "event/skip_assets.png")
    battle = module.Battle(is_tool=True)
    assert battle.fight() is False
    assert 40 < auto._frame <= 62
    assert (1400, 700) not in auto.clicks


def test_back_home_repeated_action_is_not_progress(monkeypatch):
    from test_daily_event_recovery import _BackInitMenuEventAuto
    module = importlib.import_module("tasks.base.back_init_menu")
    auto = _BackInitMenuEventAuto([[("判定成功", (500, 200, 700, 240)),
                                    ("继续", (680, 800, 760, 840))]])
    monkeypatch.setattr(module, "auto", auto)
    monkeypatch.setattr(module, "ensure_simulator_game_started", lambda: False)
    monkeypatch.setattr(module, "retry", lambda: True)
    monkeypatch.setattr(module, "sleep", lambda _: None)
    monkeypatch.setattr(module, "monotonic", lambda: auto._ocr_calls)
    assert module.back_init_menu(allow_restart=False) is False
    assert 60 <= auto._ocr_calls <= 62


@pytest.mark.parametrize("terminal", [False, True])
def test_network_interrupt_has_priority_over_event_action(monkeypatch, terminal):
    module = importlib.import_module("tasks.battle.battle")
    entries = [("判定成功", (500, 200, 700, 240)), ("继续", (680, 800, 760, 840))]
    auto = _FightEventAuto([entries] * 4)
    monkeypatch.setattr(module, "auto", auto)
    monkeypatch.setattr(module, "sleep", lambda _: None)
    monkeypatch.setattr(module, "retry", lambda: True)
    def network():
        if auto._frame <= 3:
            return False if terminal else True
        return None
    monkeypatch.setattr(module, "handle_server_error_dialog", network)
    result = module.Battle(is_tool=True).fight()
    if terminal:
        assert result is False
        assert auto.clicks == []
    else:
        assert result is None
        assert auto.clicks == [(720, 820), (1400, 700)]


def test_normal_forty_second_animation_still_settles(monkeypatch):
    module = importlib.import_module("tasks.battle.battle")
    auto = _FightEventAuto([[("判定成功", (500, 200, 700, 240))]] * 40)
    monkeypatch.setattr(module, "auto", auto)
    monkeypatch.setattr(module, "sleep", lambda _: None)
    monkeypatch.setattr(module, "monotonic", lambda: auto._frame, raising=False)
    monkeypatch.setattr(module, "handle_server_error_dialog", lambda: None)
    monkeypatch.setattr(module, "retry", lambda: True)
    assert module.Battle(is_tool=True).fight() is None
    assert auto.clicks == [(1400, 700)]
