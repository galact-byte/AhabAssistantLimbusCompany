from types import SimpleNamespace

import tasks.base.retry_monitor as monitor_module


def test_monitor_suspends_business_and_resumes_after_two_clear_frames(monkeypatch):
    calls = []
    monitor = monitor_module.RetryMonitor(click_cooldown=0)
    positions = iter([(10, 20), None, None])
    monkeypatch.setattr(monitor, "_find_retry_button", lambda _: next(positions))
    monkeypatch.setattr(monitor_module, "auto", SimpleNamespace(
        check_pause=lambda: False,
        suspend_interactions=lambda: calls.append("suspend"),
        resume_interactions=lambda: calls.append("resume"),
        monitor_mouse_click=lambda *pos: calls.append(pos),
        invalidate_screenshot_cache=lambda: calls.append("invalidate"),
    ))
    assert monitor.check_once(object()) is True
    assert calls == ["suspend", (10, 20), "invalidate"]
    assert monitor.check_once(object()) is False
    assert "resume" not in calls
    assert monitor.check_once(object()) is False
    assert calls[-1] == "resume"


def test_stop_restores_business_gate_without_thread(monkeypatch):
    calls = []
    monkeypatch.setattr(monitor_module, "auto", SimpleNamespace(resume_interactions=lambda: calls.append("resume")))
    monitor = monitor_module.RetryMonitor()
    monitor._handling_retry = True
    monitor.stop()
    assert monitor._stop_event.is_set()
    assert monitor._handling_retry is False
    assert calls == ["resume"]
