"""直接执行UI方法，替换窗口外设以避免触碰真实游戏。"""

import ast
from pathlib import Path
from types import SimpleNamespace


def load_method(path, cls, method, namespace):
    tree = ast.parse(Path(path).read_text(encoding="utf-8-sig"))
    owner = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cls)
    node = next(n for n in owner.body if isinstance(n, ast.FunctionDef) and n.name == method)
    exec(compile(ast.Module(body=[node], type_ignores=[]), path, "exec"), namespace)
    return namespace[method]


def test_stop_button_keeps_settings_locked_until_worker_exits():
    actions = []
    method = load_method(
        "app/farming_interface.py",
        "FarmingInterfaceLeft",
        "start_and_stop_tasks",
        {
            "cfg": SimpleNamespace(set_reduce_miscontact=True, simulator=False),
            "screen": SimpleNamespace(reset_win=lambda **k: actions.append("reset-window")),
            "auto": SimpleNamespace(clear_img_cache=lambda: actions.append("clear")),
            "mediator": SimpleNamespace(
                refresh_teams_order=SimpleNamespace(emit=lambda: None),
                mirror_bar_kill_signal=SimpleNamespace(emit=lambda: None),
            ),
        },
    )
    button = SimpleNamespace(
        get_text=lambda: "S t o p !",
        set_text=lambda s: actions.append(s),
        setEnabled=lambda value: actions.append(("enabled", value)),
    )
    ui = SimpleNamespace(
        link_start_button=button,
        my_script=SimpleNamespace(isRunning=lambda: True),
        _enable_setting=lambda p: actions.append("unlock"),
        parent=lambda: None,
        reset_pause_resume_button=lambda: None,
        stop_script=lambda: actions.append("request"),
    )
    method(ui)
    assert actions == ["request"]


def test_completion_exit_requests_window_close_not_sys_exit():
    actions = []
    method = load_method(
        "app/farming_interface.py",
        "FarmingInterfaceLeft",
        "stop_AALC",
        {
            "log": SimpleNamespace(debug=lambda *a: None),
            "sys": SimpleNamespace(exit=lambda code: actions.append("sys-exit")),
        },
    )
    ui = SimpleNamespace(
        after_completion_selector=SimpleNamespace(_hide_editor=lambda: None),
        window=lambda: SimpleNamespace(close=lambda: actions.append("close")),
    )
    method(ui)
    assert actions == ["close"]


def test_confirmed_window_close_waits_for_running_worker():
    actions = []
    method = load_method(
        "app/my_app.py",
        "MainWindow",
        "closeEvent",
        {
            "cfg": SimpleNamespace(set_value=lambda *a: None),
            "MessageBoxConfirm": lambda *a: SimpleNamespace(exec=lambda: True),
            "QTimer": SimpleNamespace(singleShot=lambda ms, callback: actions.append("poll")),
            "super": lambda: SimpleNamespace(closeEvent=lambda e: actions.append("destroy")),
        },
    )
    worker = SimpleNamespace(isRunning=lambda: True, terminate=lambda: actions.append("stop"))
    ui = SimpleNamespace(
        x=lambda: 0,
        y=lambda: 0,
        isVisible=lambda: True,
        tr=lambda s: s,
        window=lambda: None,
        close=lambda: actions.append("close"),
        farming_interface=SimpleNamespace(interface_left=SimpleNamespace(my_script=worker)),
        tools_interface=SimpleNamespace(tools={}),
    )
    event = SimpleNamespace(ignore=lambda: actions.append("ignore"))
    method(ui, event)
    assert actions == ["stop", "ignore", "poll"]
    actions.clear()
    method(ui, event)
    assert actions == ["ignore", "poll"]  # 重复关窗不重复确认或请求停止


def test_finished_slot_only_unlocks_and_exits_after_native_thread_finished():
    actions = []
    method = load_method(
        "app/farming_interface.py",
        "FarmingInterfaceLeft",
        "_on_script_finished",
        {
            "log": SimpleNamespace(debug=lambda *a: None),
            "mediator": SimpleNamespace(
                refresh_teams_order=SimpleNamespace(emit=lambda: None),
                mirror_bar_kill_signal=SimpleNamespace(emit=lambda: None),
            ),
        },
    )
    worker = SimpleNamespace(isRunning=lambda: True, stop_requested=False, exit_requested=True)
    ui = SimpleNamespace(
        my_script=worker,
        link_start_button=SimpleNamespace(
            setEnabled=lambda value: actions.append("enabled"), set_text=lambda text: None
        ),
        _enable_setting=lambda parent: actions.append("unlock"),
        parent=lambda: None,
        reset_pause_resume_button=lambda: None,
        stop_AALC=lambda: actions.append("exit"),
        _cleanup_stopped_session=lambda: actions.append("cleanup"),
    )
    method(ui)
    assert actions == []
    worker.isRunning = lambda: False
    method(ui)
    assert actions == ["enabled", "unlock", "exit"]
    actions.clear()
    worker.stop_requested = True
    worker.exit_requested = False
    method(ui)
    assert actions == ["cleanup", "enabled", "unlock"]
