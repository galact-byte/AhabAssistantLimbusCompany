"""业务线程的协作取消；只在 Python 安全边界退出，不中断原生推理。"""

import threading
import time
from contextlib import contextmanager

_state = threading.local()


class TaskCancelled(BaseException):
    """不让业务层的 except Exception 把停止请求当作可重试错误。"""


@contextmanager
def cancellation_scope(stop_event):
    previous = getattr(_state, "stop_event", None)
    _state.stop_event = stop_event
    try:
        yield
    finally:
        _state.stop_event = previous


def checkpoint():
    event = getattr(_state, "stop_event", None)
    if event is not None and event.is_set():
        raise TaskCancelled()


def sleep(seconds):
    event = getattr(_state, "stop_event", None)
    if event is None:
        time.sleep(seconds)
    else:
        checkpoint()
        if event.wait(seconds):
            raise TaskCancelled()
