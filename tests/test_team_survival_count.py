import ast
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.mark.parametrize("text,expected", [("5/12", True), ("9/12", True), ("12/12", True), ("5/10", True), ("4/12", False)])
def test_check_team_includes_current_twelve_member_roster(text, expected):
    path = Path(__file__).resolve().parents[1] / "tasks/teams/team_formation.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "check_team")
    method.decorator_list = []
    namespace = {"auto": SimpleNamespace(find_element=lambda candidates, **kw: text in candidates)}
    exec(compile(ast.Module(body=[method], type_ignores=[]), str(path), "exec"), namespace)
    assert namespace["check_team"]() is expected
