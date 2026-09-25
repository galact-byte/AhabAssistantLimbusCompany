"""只读提取现有离店方法，在假自动化对象上验证点击成功是否绕过预算。"""
import ast
import json
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[4]
source = ROOT / "tasks/mirror/in_shop.py"
tree = ast.parse(source.read_text(encoding="utf-8"))
method = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "in_shop")


class EndProbe(BaseException):
    pass


class FakeAuto:
    model = "clam"
    leave_attempts = 0
    return_to_menu_calls = 0

    def take_screenshot(self):
        return object()

    def mouse_click_blank(self, **kwargs):
        pass

    def click_element(self, target):
        if target.endswith("/leave_assets.png"):
            self.leave_attempts += 1
            if self.leave_attempts > 60:
                raise EndProbe()
            return True
        return False


auto = FakeAuto()

def back_init_menu():
    auto.return_to_menu_calls += 1


namespace = {
    "auto": auto,
    "sleep": lambda *_: None,
    "retry": lambda: None,
    "inspect_mirror_shop_presence": lambda _: SimpleNamespace(state="shop"),
    "should_end_shop_leave": lambda _: False,
    "back_init_menu": back_init_menu,
    "log": SimpleNamespace(info=lambda *_: None, debug=lambda *_: None, error=lambda *_: None),
}
exec(compile(ast.Module(body=[method], type_ignores=[]), str(source), "exec"), namespace)
shop = SimpleNamespace(
    ignore_shop=[False] * 5, skill_replacement=False,
    do_not_heal=True, do_not_sell=True, do_not_buy=True,
    do_not_fuse=True, do_not_enhance=True, RestartGame=RuntimeError,
)
try:
    namespace["in_shop"](shop, 1)
except EndProbe:
    pass
result = {
    "模拟离开按钮命中次数": auto.leave_attempts,
    "回初始界面次数": auto.return_to_menu_calls,
    "最终识别模式": auto.model,
    "结论": "60次已完成点击后仍未耗尽30次预算；第61次由探针主动终止。",
}
assert auto.leave_attempts == 61
assert auto.return_to_menu_calls == 0
assert auto.model == "clam"
print(json.dumps(result, ensure_ascii=False, indent=2))
