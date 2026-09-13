"""隔离进程验证真实 Qt/ONNX 生命周期；合成输入不是游戏截图，不操作游戏。"""

import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import cv2
import numpy as np
from PySide6.QtCore import QCoreApplication

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from module.ocr import ocr  # noqa: E402
from tasks.base import script_task_scheme as scheme  # noqa: E402


def main():
    app = QCoreApplication.instance() or QCoreApplication([])
    image = np.full((900, 1600, 3), 255, dtype=np.uint8)
    for y in range(100, 850, 100):
        cv2.putText(image, "AALC safe stop 123", (100, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
    native_engine = ocr.engine
    scheme.cfg = SimpleNamespace(get_value=lambda *args: False)
    scheme.retry_monitor = SimpleNamespace(stop=lambda: None, request_stop=lambda: None)
    scheme.auto = SimpleNamespace(clear_img_cache=lambda: None)
    rows = []
    for cycle in range(6):
        entered = threading.Event()
        returned = threading.Event()
        actions = []

        def engine(frame):
            entered.set()
            try:
                return native_engine(frame)
            finally:
                returned.set()

        def task():
            ocr.run(image)
            actions.append("after-ocr")

        ocr.engine = engine
        scheme.script_task = task
        worker = scheme.my_script_task()
        finished = []
        worker.finished.connect(lambda: finished.append(True))
        started = time.monotonic()
        worker.start()
        assert entered.wait(10), "ONNX调用未开始"
        should_stop = cycle % 2 == 0
        if should_stop:
            # 留出进入真实推理的时间，不通过强杀制造崩溃。
            time.sleep(0.01)
            assert not returned.is_set(), "输入太短，未覆盖推理期间停止"
            worker.terminate()
            worker.terminate()  # 重复停止必须幂等
            assert worker.isRunning(), "原生调用尚未返回时线程被提前结束"
        assert worker.wait(20000), "线程未能安全退出"
        app.processEvents()
        assert returned.is_set()
        assert finished == [True]
        assert actions == ([] if should_stop else ["after-ocr"])
        assert not worker.exit_requested
        assert not hasattr(worker, "exception"), getattr(worker, "exception", None)
        rows.append({"cycle": cycle + 1, "stop": should_stop, "seconds": round(time.monotonic() - started, 3)})
    sys.stdout.write(f"NATIVE_STOP_PROBE_OK {rows}\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
