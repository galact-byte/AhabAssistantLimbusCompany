from __future__ import annotations

import importlib
from types import SimpleNamespace


class _RecordingSignal:
    """Minimal stand-in for a Qt Signal that counts emissions."""

    def __init__(self) -> None:
        self.emitted = 0

    def emit(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        self.emitted += 1


def _make_worker(monkeypatch, script_task_return):
    scheme = importlib.import_module("tasks.base.script_task_scheme")

    fake_mediator = SimpleNamespace(
        kill_signal=_RecordingSignal(),
        request_focus=_RecordingSignal(),
        script_finished=_RecordingSignal(),
    )
    monkeypatch.setattr(scheme, "mediator", fake_mediator)
    monkeypatch.setattr(scheme, "script_task", lambda: script_task_return)
    monkeypatch.setattr(scheme, "cfg", SimpleNamespace(get_value=lambda *_a, **_k: False))
    monkeypatch.setattr(scheme.auto, "clear_img_cache", lambda: None)

    worker = scheme.my_script_task.__new__(scheme.my_script_task)
    return scheme, worker, fake_mediator


def test_run_does_not_exit_aalc_when_task_sequence_fails(monkeypatch) -> None:
    # 任务失败时 script_task 返回 False；False == 0 曾误触发退出信号。
    _scheme, worker, fake_mediator = _make_worker(monkeypatch, False)

    worker._run()

    assert fake_mediator.kill_signal.emitted == 0


def test_run_does_not_exit_aalc_when_completed_without_exit_action(monkeypatch) -> None:
    # 成功但未配置"退出AALC"时 script_task 返回 None，不应退出。
    _scheme, worker, fake_mediator = _make_worker(monkeypatch, None)

    worker._run()

    assert fake_mediator.kill_signal.emitted == 0


def test_run_exits_aalc_when_exit_action_requested(monkeypatch) -> None:
    # 成功且配置了"退出AALC"时，script_task 返回退出哨兵，应触发退出信号。
    scheme, worker, fake_mediator = _make_worker(monkeypatch, True)

    worker._run()

    assert fake_mediator.kill_signal.emitted == 1
    # 哨兵语义应稳定：退出请求用 True 表达，不再复用 0。
    assert scheme.EXIT_AALC_SENTINEL is True
