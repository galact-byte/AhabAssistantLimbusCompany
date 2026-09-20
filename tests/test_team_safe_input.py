from types import SimpleNamespace

import pytest

from module.automation.input_handlers import input as inputs


@pytest.fixture
def io(monkeypatch):
    calls = []
    monkeypatch.setattr(inputs, "screen", SimpleNamespace(handle=SimpleNamespace(
        hwnd=123, isMinimized=False, rect=lambda *_: (100, 200, 1700, 1100))))
    monkeypatch.setattr(inputs, "sleep", lambda *_: None)
    for cls in (inputs.Input, inputs.BackgroundInput, inputs.WindowMoveInput):
        monkeypatch.setattr(cls, "wait_pause", lambda _: None)
        monkeypatch.setattr(cls, "get_mouse_position", lambda _: (800, 700))
    monkeypatch.setattr(inputs.BackgroundInput, "set_active", lambda _: None)
    monkeypatch.setattr(inputs.BackgroundInput, "set_mouse_pos", lambda *a, **k: calls.append(("move", a[1:])))
    monkeypatch.setattr(inputs.BackgroundInput, "mouse_move", lambda *a: calls.append(("restore", a[1])))
    for name in ("mouse_down", "mouse_up"):
        monkeypatch.setattr(inputs.BackgroundInput, name, lambda *a: pytest.fail("编队滚动不能按左键"))
    monkeypatch.setattr(inputs.pyautogui, "mouseDown", lambda: pytest.fail("编队滚动不能按左键"))
    monkeypatch.setattr(inputs.pyautogui, "mouseUp", lambda: pytest.fail("编队滚动不能按左键"))
    monkeypatch.setattr(inputs.pyautogui, "moveTo", lambda *a, **k: calls.append(("move", a)))
    monkeypatch.setattr(inputs.pyautogui, "scroll", lambda *a, **k: calls.append(("wheel", a)))
    for obj, name in ((inputs.win32api, "PostMessage"), (inputs.win32gui, "SendMessage")):
        monkeypatch.setattr(obj, name, lambda *a: calls.append(("message", a)))
    return calls


@pytest.mark.parametrize("post", [False, True])
def test_background_team_scroll_is_wheel_at_list_client_position(io, post):
    handler = inputs.BackgroundInput()
    handler.use_post_message = post
    # 旧接口也必须安全，不能让遗漏的调用点继续拖动条目。
    assert handler.mouse_swipe_for_team_scroll(150, 450, dy=-385) is True
    messages = [args for name, args in io if name == "message"]
    assert len(messages) == 1
    _, msg, wparam, lparam = messages[0]
    assert msg == inputs.win32con.WM_MOUSEWHEEL
    assert (lparam & 65535, (lparam >> 16) & 65535) == (250, 650)
    assert ((wparam >> 16) & 65535) == ((-120) & 65535)
    assert io[-1] == ("restore", (800, 700))


def test_foreground_team_scroll_moves_to_list_and_restores_mouse(io):
    assert inputs.Input().mouse_swipe_for_team_scroll(150, 450, dy=400) is True
    assert ("move", (250, 650)) in io
    assert ("wheel", (1,)) in io
    assert io[-1] == ("move", (800, 700))


@pytest.mark.parametrize("cls", [inputs.Input, inputs.BackgroundInput, inputs.WindowMoveInput])
def test_team_scroll_checks_pause_before_any_input(io, monkeypatch, cls):
    class Paused(BaseException):
        pass

    def wait(_):
        raise Paused()

    monkeypatch.setattr(cls, "wait_pause", wait)
    with pytest.raises(Paused):
        cls().mouse_swipe_for_team_scroll(150, 450, dy=-1)
    assert not io


def test_background_cursor_restored_when_message_raises(io, monkeypatch):
    def fail(*args):
        raise OSError("message unavailable")

    handler = inputs.BackgroundInput()
    handler.use_post_message = False
    monkeypatch.setattr(inputs.win32gui, "SendMessage", fail)
    with pytest.raises(OSError):
        handler.mouse_swipe_for_team_scroll(150, 450, dy=-1)
    assert io[-1] == ("restore", (800, 700))


def test_background_no_window_fails_without_input(io, monkeypatch):
    monkeypatch.setattr(inputs.screen.handle, "hwnd", None)
    assert inputs.BackgroundInput().mouse_swipe_for_team_scroll(150, 450, dy=-1) is False
    assert not io


def test_window_move_team_scroll_fails_without_dragging(io, monkeypatch):
    monkeypatch.setattr(inputs.WindowMoveInput, "_set_window_pos", lambda *a: pytest.fail("不应移动窗口拖动"))
    assert inputs.WindowMoveInput().mouse_swipe_for_team_scroll(150, 450, dy=-400) is False


def test_automation_team_scroll_uses_interaction_gate(io):
    import threading

    from module.automation.automation import Automation

    automation = object.__new__(Automation)
    automation._input_lock = threading.RLock()
    handler = inputs.Input()
    automation.input_handler = handler
    gate_calls = []
    automation._interaction_gate = SimpleNamespace(
        wait=lambda **kw: gate_calls.append("wait") or True,
        is_set=lambda: True,
    )
    action = automation._run_business_interaction("mouse_swipe_for_team_scroll")
    assert action(150, 450, dy=-1) is True
    assert gate_calls == ["wait"]
    assert ("wheel", (-1,)) in io


def test_foreground_cursor_restored_when_wheel_raises(io, monkeypatch):
    def fail(*args):
        raise OSError("wheel unavailable")
    monkeypatch.setattr(inputs.pyautogui, "scroll", fail)
    with pytest.raises(OSError):
        inputs.Input().mouse_swipe_for_team_scroll(150, 450, dy=-400)
    assert io[-1] == ("move", (800, 700))
