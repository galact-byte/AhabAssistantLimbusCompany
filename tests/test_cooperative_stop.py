"""停止必须让原生调用返回，而不是强杀工作线程。"""

import importlib
import threading
from types import SimpleNamespace


def test_stop_requests_interruption_without_native_terminate(monkeypatch):
    scheme = importlib.import_module("tasks.base.script_task_scheme")
    calls = []
    worker = scheme.my_script_task()
    monkeypatch.setattr(scheme.retry_monitor, "stop", lambda: calls.append("join"))
    monkeypatch.setattr(scheme.auto, "reset_safety_locks", lambda: calls.append("replace-locks"))
    worker.terminate()
    assert worker.stop_requested is True
    assert calls == []


def test_cancelled_sleep_unwinds_without_swallowing_business_error_handlers():
    import pytest

    from module.task_control import TaskCancelled, cancellation_scope, sleep

    stop = threading.Event()
    stop.set()
    with cancellation_scope(stop), pytest.raises(TaskCancelled):
        try:
            sleep(60)
        except Exception:
            raise AssertionError("普通错误处理不应吞掉取消")
    sleep(0)  # 退出scope不能污染下一任务或UI线程


def test_monitor_retains_live_thread_until_join_completes(monkeypatch):
    module = importlib.import_module("tasks.base.retry_monitor")
    monitor = module.RetryMonitor()
    entered, release = threading.Event(), threading.Event()
    monitor._thread = threading.Thread(target=lambda: (entered.set(), release.wait(10)))
    monitor._thread.start()
    assert entered.wait(2)
    old_thread = monitor._thread
    stopper = threading.Thread(target=monitor.stop)
    stopper.start()
    try:
        stopper.join(2.2)
        assert monitor._thread is old_thread
        assert stopper.is_alive()
    finally:
        release.set()
        stopper.join(3)
        old_thread.join(3)
    assert monitor._thread is None


def test_monitor_stop_unwinds_a_paused_input(monkeypatch):
    module = importlib.import_module("tasks.base.retry_monitor")
    from module.task_control import sleep

    monitor = module.RetryMonitor(poll_interval=0.01)
    entered = threading.Event()

    def paused_input():
        entered.set()
        sleep(3)

    monkeypatch.setattr(monitor, "check_once", paused_input)
    monitor._thread = threading.Thread(target=monitor._run)
    monitor._thread.start()
    assert entered.wait(2)
    stopper = threading.Thread(target=monitor.stop)
    stopper.start()
    stopper.join(1)
    try:
        assert not stopper.is_alive(), "暂停输入阻塞了监控停止"
    finally:
        stopper.join(5)


def test_stop_waits_for_native_boundary_then_unwinds(monkeypatch):
    scheme = importlib.import_module("tasks.base.script_task_scheme")
    entered, release = threading.Event(), threading.Event()
    steps = []
    worker = scheme.my_script_task()

    def task():
        entered.set()
        release.wait(5)  # 模拟不能中断的原生调用
        from module.task_control import checkpoint

        checkpoint()
        steps.append("unsafe-next-action")

    monkeypatch.setattr(scheme, "script_task", task)
    monkeypatch.setattr(scheme, "cfg", SimpleNamespace(get_value=lambda *a: False))
    monkeypatch.setattr(scheme.retry_monitor, "stop", lambda: steps.append("monitor-joined"))
    monkeypatch.setattr(scheme.auto, "clear_img_cache", lambda: steps.append("cache-cleared"))
    runner = threading.Thread(target=worker.run)
    runner.start()
    assert entered.wait(2)
    try:
        worker.terminate()
        assert runner.is_alive()
        assert steps == []
    finally:
        release.set()
        runner.join(3)
    assert not runner.is_alive()
    assert steps == ["monitor-joined", "cache-cleared"]
