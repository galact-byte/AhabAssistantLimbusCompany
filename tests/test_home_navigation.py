import pytest

from tasks.event_page import resolve_event_page


def test_standalone_skip_does_not_authorize_an_event_action():
    assert resolve_event_page([("SKIP", (1380, 796, 1455, 824))]) is None


@pytest.mark.parametrize("entries,expected", [
    ([("玻璃窗", (20, 800, 100, 850)), ("驾驶席", (200, 800, 280, 850))], (240, 825)),
    ([("驾驶席", (200, 800, 280, 850))], None),
    ([("玻璃窗", (20, 20, 100, 50)), ("驾驶席", (200, 800, 280, 850))], None),
    ([("玻璃窗", (20, 800, 100, 850)), ("前往驾驶席", (200, 800, 280, 850))], None),
])
def test_home_navigation_requires_two_aligned_tabs(entries, expected):
    from tasks.base.home_page import find_home_drive
    assert find_home_drive(entries) == expected
