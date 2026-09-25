# 2026-09-25 集成验证

- 选队先 RED：`tests/test_team_list_parser.py::test_logged_900p_top_row_is_retained` 在旧门限下首行被误认 `编队#2`；改为 `6 * scale` 后连同标题重叠、缺行和编队选择共 50 项通过。两张原始 PNG 使用 `Automation.get_ocr_entries()` + `read_team_list(..., (1505.75, 223.125), 0.625)` 实际重放，首行均为 `剧情关卡`，`first_row_at_top=True`。
- 上游先 RED：`tests/test_feature_matching_input_guards.py` 三类空输入和缓存清理共 4 项失败，原始失败原因见子任务 `research/red-feature-guards.md`；合并 `ddc2204` 后 4 项转绿，新增“资源可用后清缓存重新匹配”共 5 项通过。
- 合并前后 `.venv/Scripts/python.exe -m pytest tests -q` 分别为 309 passed、314 passed；Ruff 范围检查、compileall、`git diff HEAD --check` 通过。`MERGE_HEAD=ddc2204`，无 unmerged 路径，季节图片 Git blob 与上游一致，图片 2560x1440 可由 PIL 校验。
- 只核对本地源和日志，不操作游戏或 G 盘安装版。09-05 核心代码/回归已在仓库，但其真实夜间商店/后台 farthest 验收未完成；09-13 已发布代码仍缺游戏实机与历史 ONNX 原生崩溃证据，均不能归档。
