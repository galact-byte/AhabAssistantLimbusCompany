"""上游融合后的生命周期与恢复边界回归，不操作真实游戏。"""

import importlib
from types import SimpleNamespace

import pytest
from test_stop_ui_lifecycle import load_method


def test_queue_is_notified_only_after_worker_has_finished():
    calls = []
    method = load_method(
        "app/farming_interface.py", "FarmingInterfaceLeft", "_on_script_finished",
        {
            "log": SimpleNamespace(debug=lambda *_: None),
            "mediator": SimpleNamespace(**{
                name: SimpleNamespace(emit=lambda name=name: calls.append(name))
                for name in ("refresh_teams_order", "mirror_bar_kill_signal", "script_finished")
            }),
        },
    )
    worker = SimpleNamespace(isRunning=lambda: True, stop_requested=False, exit_requested=False)
    ui = SimpleNamespace(
        my_script=worker,
        link_start_button=SimpleNamespace(setEnabled=lambda _: None, set_text=lambda _: None),
        _enable_setting=lambda _: None, parent=lambda: None, reset_pause_resume_button=lambda: None,
    )
    method(ui)
    assert calls == []
    worker.isRunning = lambda: False
    method(ui)
    assert calls == ["refresh_teams_order", "mirror_bar_kill_signal", "script_finished"]


@pytest.mark.parametrize("age, window, alive, killed", [
    (10, 0, True, False), (179, 0, True, False), (180, 0, False, True),
    (181, 0, False, True), (900, 123, True, False),
])
def test_game_process_grace_period_and_missing_window(monkeypatch, age, window, alive, killed):
    module = importlib.import_module("module.game_and_screen.game")
    operations = []
    game = object.__new__(module.Game)
    game.process_name = "LimbusCompany"
    game.log = SimpleNamespace(debug=lambda *_: None, warning=lambda *_: None)
    process = SimpleNamespace(info={"name": "limbuscompany.EXE"}, pid=42, create_time=lambda: 1000 - age)
    monkeypatch.setattr(module.psutil, "process_iter", lambda _: [process])
    monkeypatch.setattr(module.psutil, "Process", lambda pid: SimpleNamespace(kill=lambda: operations.append(pid)))
    monkeypatch.setattr(module.win32gui, "FindWindow", lambda *_: window)
    monkeypatch.setattr(module, "time", lambda: 1000)
    assert game.check_game_alive() is alive
    assert operations == ([42] if killed else [])


@pytest.mark.parametrize("configured, expected", [(120, 120), (1, 30), ("invalid", 90), (None, 90)])
def test_configurable_stall_timeout(monkeypatch, configured, expected):
    module = importlib.import_module("tasks.base.retry")
    monkeypatch.setattr(module, "cfg", SimpleNamespace(get_value=lambda *a: configured))
    assert module.get_task_stall_timeout() == expected


def test_return_home_uses_configured_timeout_and_one_owned_restart(monkeypatch):
    from test_daily_event_recovery import _BackInitMenuEventAuto
    module = importlib.import_module("tasks.base.back_init_menu")
    retry = importlib.import_module("tasks.base.retry")
    clock = iter((0, 91, 121))
    calls = []
    monkeypatch.setattr(module, "auto", _BackInitMenuEventAuto([[]]))
    monkeypatch.setattr(module, "retry", lambda: True)
    monkeypatch.setattr(module, "ensure_simulator_game_started", lambda: False)
    monkeypatch.setattr(module, "monotonic", lambda: next(clock))
    monkeypatch.setattr(module, "get_task_stall_timeout", lambda: 120)
    monkeypatch.setattr(retry, "restart_game", lambda **kw: calls.append(kw) or True)
    assert module.back_init_menu() is True
    assert calls == [{"close_first": True}]
