"""执行真实商店方法；仅替换游戏 I/O，捕获成功点击绕过预算的回归。"""
import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from tasks.mirror.shop_presence import resolve_shop_leave_dialog


@pytest.mark.parametrize("screenshot_available", [True, False])
@pytest.mark.parametrize("dialog_visible", [True, False])
@pytest.mark.parametrize("recovery_ok", [True, False])
@pytest.mark.parametrize("outcome", ["stuck", "map", "retry_failure"])
def test_shop_leave_cannot_spin_forever(screenshot_available, dialog_visible, recovery_ok, outcome):
    source = Path(__file__).resolve().parents[1] / "tasks/mirror/in_shop.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "in_shop")
    frames = 0
    recovered = []

    def screenshot():
        nonlocal frames
        frames += 1
        assert frames <= 100, "离店无进展超过100帧，恢复预算被绕过"
        return object() if frames == 1 or screenshot_available else None

    def click(target):
        if dialog_visible:
            assert not target.endswith("/leave_assets.png"), "弹窗存在时不能点底层离开"
        return target.endswith("/leave_assets.png")

    auto = SimpleNamespace(
        model="clam", take_screenshot=screenshot,
        mouse_click_blank=lambda **_: None,
        click_element=click,
        get_ocr_entries=lambda: [("要离开商店吗？", (600, 400, 900, 450))] if dialog_visible else [],
    )
    def recover(**kwargs):
        recovered.append(kwargs)
        return recovery_ok

    namespace = {
        "auto": auto, "sleep": lambda *_: None,
        "retry": lambda: False if outcome == "retry_failure" else None,
        "resolve_shop_leave_dialog": resolve_shop_leave_dialog,
        "inspect_mirror_shop_presence": lambda _: SimpleNamespace(state="shop", reason="test"),
        "should_end_shop_leave": lambda _: outcome == "map",
        "back_init_menu": recover,
        "log": SimpleNamespace(info=lambda *_: None, debug=lambda *_: None, error=lambda *_: None),
    }
    exec(compile(ast.Module(body=[method], type_ignores=[]), str(source), "exec"), namespace)
    shop = SimpleNamespace(
        ignore_shop=[False] * 5, skill_replacement=False,
        do_not_heal=True, do_not_sell=True, do_not_buy=True,
        do_not_fuse=True, do_not_enhance=True, RestartGame=RuntimeError,
    )
    result = namespace["in_shop"](shop, 1)
    if outcome == "retry_failure" and screenshot_available:
        assert recovered == []
        assert result is False
    elif outcome == "map" and screenshot_available:
        assert recovered == []
        assert result is None
    else:
        assert recovered == [{"allow_restart": False}]
        assert result is recovery_ok
