# 选队全链路核对矩阵（2026-09-26）

| 路径/边界 | 源码 | 证据/测试 | 结论 |
| --- | --- | --- | --- |
| Windows 900p 后台日常队伍1，顶部“剧情关卡”且滚轮不动 | `tasks/team_list.py`, `tasks/teams/team_formation.py` | 原始截图和日志见 `log-comparison.md`；`test_recorded_900p_top_rows_select_without_unresponsive_wheel` RED→GREEN | 修复：直接选择并核验，跳过无效滚轮探针 |
| 按顺序第2项名称可以是 #3 / 已知顶部第2项 | 同上 | `test_order_uses_current_second_item_not_number_two_and_corrects_wrong_click`, `test_recorded_900p_top_rows_select_without_unresponsive_wheel` | 通过；不混淆序号与名称 |
| OCR 标题重叠/首项未知/行缺失或重名 | `tasks/team_list.py:read_team_list`, `TeamListPage.has_known_top_anchor` | `test_team_list_parser.py`, `test_top_geometry_without_known_first_item_cannot_authorize_ordered_click`, `test_uncertain_selection_fails_with_finite_budget` | 保守失败，不以残缺序列授权点击 |
| 中途滚动停在非顶部但首行几何像顶部 | `tasks/teams/team_formation.py:_reset_team_list` | `test_scroll_stopping_mid_list_cannot_masquerade_as_top` RED→GREEN | 修复：必须识别固定首项；不能把中途项当第1项 |
| 目标不在首屏/向上归顶/分页重叠/真实位移 | `_reset_team_list`, `_scan_team_order` | `test_team_visual_selection.py` 中 `upward_scroll_failure`, `scroll_stopping_mid_list`, `test_observed_displacement_not_assumed_wheel_pixel_distance`, `absent`, `stuck`，`test_team_list_parser.py` 页间扩展 | 模拟回归通过；实机后台非首屏滚轮消费未证实，停滞则有界失败 |
| 按名称编号：唯一命中、重复、不存在、第40项边界 | `tasks/team_list.py:matches_team_number`, `select_battle_team` | `test_team_name_selection.py`, `test_team_visual_selection.py` named/boundary tests | 模拟回归通过；不需每次扫描全部40槽 |
| 选后标题/误点/截图失败/失败帧 | `selected_team_matches`, `_team_selection_failed` | `test_team_visual_selection.py` wrong_clicks、bad_screenshot 等 | 有限核验；未经标题证实不报成功 |
| Windows 前后台轮滚、window_move 失败、模拟器 | `module/automation/input_handlers/input.py` | `test_team_safe_input.py`, `test_simulator_keeps_specialized_gesture_path` | 无条目左键拖动；实机 Windows WM_MOUSEWHEEL 是否被游戏消费未知 |
| 日常 EXP/Thread 单场、组、顶层 | `tasks/base/script_task_scheme.py`, `tasks/daily/luxcavation.py` | `test_daily_team_selection.py` 进本失败、选队失败、成功及组中断；其他 top-level tests | 回归通过；失败不进入战斗或错误完成 |
| 镜牢选队连续失败 | `tasks/mirror/mirror.py:select_mirror_team` | `test_mirror_failure_never_confirms_or_loads_team_code` | 拒绝后不确认/加载编队码；有限重试并抛错 |
| 镜牢选队成功但确认超时/恢复失败 | 同上；`tasks/base/script_task_scheme.py:onetime_mir_process` | `test_mirror_team_confirmation_failure_is_terminal` 双分支 RED→GREEN；`test_mirror_team_confirmation_exception_stops_top_level` | 修复：抛错并在顶层返回 False，不继续成功收尾 |
| 镜牢成功进入星光页 | `Mirror.select_mirror_team` | `test_mirror_team_confirmation_reaches_coins` | 保持正常成功路径 |
| 实机长时间无人值守 | G 盘两套安装保持只读 | 本地失败日志和上游成功日志，只说明当次情况；本轮仅发现 `LimbusCompany` 进程运行，未注入点击 | 未验证；本仓库修改未部署到 G 盘，不能宣称整夜稳定 |

完整回归：本任务最新全库 pytest 与 Ruff 结果见 `implement.md`。各项“通过”仅指所列模拟/静态验证，不等价于游戏实机证据。
