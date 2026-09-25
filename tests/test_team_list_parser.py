import pytest

from tasks.team_list import read_team_list, selected_team_matches


def entries_at_scale(scale):
    return [(text, tuple(value * scale for value in bounds)) for text, bounds in [
        ("编队", (200, 552, 288, 587)),
        ("剧情关卡", (160, 624, 328, 656)),
        ("我的队伍", (160, 696, 328, 728)),
        ("编队#3", (160, 768, 328, 800)),
        ("预设#1", (160, 288, 304, 328)),
        ("我的队伍", (640, 64, 960, 112)),
    ]]


@pytest.mark.parametrize("scale", [0.5, 0.625, 0.75, 1])
def test_parser_preserves_custom_names_and_excludes_title_and_preset(scale):
    page = read_team_list(entries_at_scale(scale), (2400 * scale, 355.2 * scale), scale)
    assert page.names == ("剧情关卡", "我的队伍", "编队#3")
    assert page.first_row_at_top
    assert page.rows[1].position == (244 * scale, 712 * scale)


def test_logged_900p_top_row_is_retained():
    # 两张 2026-09-25 失败截图的 OCR 边框；仅第二张的 #2 横坐标差 1px。
    for second_left in (132, 133):
        entries = [
            ("编队", (140, 344, 184, 371)),
            ("剧情关卡", (130, 377, 199, 402)),
            ("编队#2", (second_left, 422, 195, 447)),
            ("编队#3", (133, 468, 195, 492)),
            ("编队#4", (133, 513, 195, 537)),
        ]
        page = read_team_list(entries, (1505.75, 223.125), 0.625)
        assert page is not None
        assert page.names[:2] == ("剧情关卡", "编队#2")
        assert page.first_row_at_top


def test_header_overlap_is_not_treated_as_first_row():
    entries = [
        ("编队", (140, 344, 184, 371)),
        ("剧情关卡", (130, 371, 199, 402)),
        ("编队#2", (132, 422, 195, 447)),
        ("编队#3", (133, 468, 195, 492)),
    ]
    page = read_team_list(entries, (1505.75, 223.125), 0.625)
    assert page is not None
    assert page.names[0] == "编队#2"
    assert not page.first_row_at_top


def test_missing_middle_row_does_not_renumber_later_rows():
    entries = entries_at_scale(1)
    del entries[2]
    assert read_team_list(entries, (2400, 355.2), 1) is None


def test_missing_header_cannot_authorize_list_clicks():
    assert read_team_list(entries_at_scale(1)[1:], (2400, 355.2), 1) is None


def test_list_text_is_not_selected_title_evidence():
    entries = entries_at_scale(1)
    assert selected_team_matches(entries, "我的队伍", (2400, 355.2), 1)
    assert not selected_team_matches(entries[:-1], "我的队伍", (2400, 355.2), 1)
    assert not selected_team_matches(entries, "编队#3", (2400, 355.2), 1)


def test_ambiguous_title_is_rejected():
    entries = entries_at_scale(1) + [("我的队伍", (200, 60, 380, 100))]
    assert not selected_team_matches(entries, "我的队伍", (2400, 355.2), 1)
