import ast
from pathlib import Path
from types import SimpleNamespace

import pytest


def test_shop_failure_reaches_mirror_recovery_boundary():
    path = Path(__file__).resolve().parents[1] / "tasks/mirror/mirror.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "in_shop")
    method.decorator_list = []
    namespace = {"cannotOperateGameError": RuntimeError}
    exec(compile(ast.Module(body=[method], type_ignores=[]), str(path), "exec"), namespace)
    mirror = SimpleNamespace(floor=5, shop=SimpleNamespace(in_shop=lambda floor: False))
    with pytest.raises(RuntimeError):
        namespace["in_shop"](mirror)
