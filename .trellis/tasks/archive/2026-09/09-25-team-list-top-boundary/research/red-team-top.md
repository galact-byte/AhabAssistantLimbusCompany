# 编队列表归顶回归：RED

执行：`.venv/Scripts/python.exe -m pytest tests/test_team_list_parser.py -q`

输出：`1 failed, 9 passed in 0.28s`。失败项 `test_logged_900p_top_row_is_retained`：期望首两项 `('剧情关卡', '编队#2')`，实际 `('编队#2', '编队#3')`。输入直接取自两张 2026-09-25 原始失败截图的 OCR 位置。标题重叠反例通过。原始完整输出见本轮命令记录；此处仅摘结论。
