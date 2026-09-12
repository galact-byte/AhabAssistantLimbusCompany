import ast
from pathlib import Path
from types import SimpleNamespace

import pytest


def test_theme_pack_failure_stops_floor_progress():
    path = Path(__file__).resolve().parents[1] / "tasks/mirror/mirror.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    branch = next(n for n in ast.walk(tree) if isinstance(n, ast.If) and isinstance(n.test, ast.Call)
                  and len(n.body) > 1 and n.test.args and isinstance(n.test.args[0], ast.Constant)
                  and n.test.args[0].value == "mirror/theme_pack/feature_theme_pack_assets.png")
    # 在真实分支中执行到失败调用边界，后续楼层计时不得发生。
    source = ast.Module(body=[ast.While(test=ast.Constant(True), body=branch.body + [ast.Break()], orelse=[])], type_ignores=[])
    mirror = SimpleNamespace(hard_mode=False, floor=1, team_order=1, use_custom_theme_pack_weight=False,
                             get_which_floor=lambda *_: None, _enter_hard_mode_if_needed=lambda: None)
    namespace = {"self": mirror, "sleep": lambda *_: None, "select_theme_pack": lambda *_: False,
                 "switch_theme_pack_difficulty": lambda *_: None, "cannotOperateGameError": RuntimeError}
    mirror.re_formation_each_floor = False
    mirror.floor_times = [0] * 5
    namespace.update(time=SimpleNamespace(time=lambda: 1), main_loop_count=0)
    # 去掉循环末尾continue防止旧实现反复执行；保留完整业务分支。
    source.body[0].body = [n for n in branch.body if not isinstance(n, ast.Continue)] + [ast.Break()]
    with pytest.raises(RuntimeError):
        exec(compile(ast.fix_missing_locations(source), str(path), "exec"), namespace)
