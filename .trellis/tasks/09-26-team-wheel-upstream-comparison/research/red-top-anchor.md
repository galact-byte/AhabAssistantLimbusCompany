# RED：2026-09-26 选队链路

- 顶部且滚轮无效：`.venv/Scripts/python.exe -m pytest -q tests/test_team_visual_selection.py -k 'recorded_900p_top_rows or top_geometry_without_known_first_item'` → exit 1，`F.`，1 failed、1 passed、29 deselected。`select_battle_team(1)` 返回 False，日志 `ValueError: 无法确认编队滚轮生效`，而失去首项身份的反例已通过。受控输入参考 G 盘原始截图的“编队”标题 344..371、剧情关卡 377..402、编队#2 422..447 的 OCR 几何；`ListScreen.stuck=True` 模拟消息已发但列表不动。
- 纯解析锚点：`.venv/Scripts/python.exe -m pytest -q tests/test_team_list_parser.py -k known_first_entry_requires_name_and_top_geometry` → exit 1，1 failed、10 deselected，`AttributeError: 'TeamListPage' object has no attribute 'has_known_top_anchor'`。
- 中途伪归顶：`.venv/Scripts/python.exe -m pytest -q tests/test_team_visual_selection.py -k scroll_stopping_mid_list_cannot_masquerade_as_top` → exit 1，1 failed、31 deselected。向上滚动限制在第17项附近、下滚/回滚正常时，旧代码仅凭首行位置认作已归顶，`select_battle_team(2)` 错误返回 True（预期 False）。
- 镜牢确认超时：`.venv/Scripts/python.exe -m pytest -q tests/test_team_visual_selection.py -k mirror_team_confirmation_timeout_is_terminal` → exit 1，1 failed、32 deselected。日志报“无法进入镜牢,尝试回到初始界面”，方法却正常返回；随后扩充为 `retry_ok=True/False` 双分支 RED（exit 1、2 failed、32 deselected），要求抛 `cannotOperateGameError`。

以上运行均在相应产品代码修改之前执行；见对应测试及 `research/log-comparison.md`。模拟屏幕的 OCR 几何取自原始失败截图，测试不发送真实游戏输入，也不等价于实机挂机结果。
