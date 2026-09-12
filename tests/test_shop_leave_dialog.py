from tasks.mirror import shop_presence


def test_leave_dialog_requires_context_and_button_geometry():
    parse = getattr(shop_presence, "resolve_shop_leave_dialog", None)
    assert callable(parse), "缺少离店弹窗识别边界"
    title = ("要离开商店吗？", (600, 400, 900, 450))
    cancel = ("取消", (600, 550, 680, 600))
    confirm = ("确认", (820, 550, 900, 600))
    assert parse([title, cancel, confirm]) == (True, (860, 575))
    assert parse([cancel, confirm]) == (False, None)
    assert parse([title, cancel]) == (True, None)
    assert parse([title, cancel, ("确认", (820, 100, 900, 150))]) == (True, None)
    assert parse([title, cancel, confirm, ("确认", (920, 550, 980, 600))]) == (True, None)
