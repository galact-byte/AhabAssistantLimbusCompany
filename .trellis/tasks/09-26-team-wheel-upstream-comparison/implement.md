# 实施与验证计划

- [x] 记录两版配置的相关输入模式与真实日志时间线，保留原始证据路径；梳理共享选队调用方及 `.trellis/spec/backend/` 规则。建立日常/镜牢 × 顺序/编号 × 首屏/非首屏/末页 × 输入模式 × 选后标题/失败传播的审计矩阵，逐条写明源码路径、真实或测试证据与未覆盖项，避免局部通过即结项。见 `research/log-comparison.md` 和 `research/selection-matrix.md`；仅提取相关输入模式，不复制日志内全部用户配置。
- [x] RED：使用此次 1600x900 截图的 OCR 几何构造可重复测试（不要依赖 G 盘在 CI 存在）；断言首项已知、目标可见时队 1/2 无需滚轮仍可点击并核验。另测当前页非顶部、缺行/重复、错误标题、后台滚轮不响应时不能误报成功；保存失败输出至本任务 `research/`。详见 `research/red-top-anchor.md`。
- [x] GREEN：为顺序模式增加经明确顶部身份验证的首屏快捷路径，不绕过选后核验；只在可观察滚动已证实时向目标继续。同步修正中途伪归顶及镜牢确认失败传播。非首屏没有被证明安全有效的实机替代输入，保留有界失败，不回退旧拖动。
- [x] 回归：`.venv/Scripts/python.exe -m pytest -q`：322 passed in 14.87s；`.venv/Scripts/python.exe -m ruff check tasks/team_list.py tasks/teams/team_formation.py module/automation/input_handlers/input.py tests --ignore E722`：通过；镜牢文件 `--ignore E722,E712,F841`：通过，E712/F841 共5条原有告警在 `git show HEAD:tasks/mirror/mirror.py` 中已存在；`git diff --check`：通过。原始 PNG 使用同套 RapidOCR 重放：锚点 True，7 行，首两行中心 y=389.5/434.5；分支审计见 `research/selection-matrix.md`。
- [ ] 实机输入验收：当前检测到 `LimbusCompany` 进程正在运行，未获操作正在运行游戏/消耗资源许可，不注入真实输入；G 盘两套发行版保持只读。需要在可用的受控窗口中确认 900p 后台非首屏滚轮消费、日常与镜牢选队，以及实际队伍顺序不变；完成前不能称夜间挂机已修好，任务保持 active。
- [x] 主会话完成 `trellis-check` 与规范复盘，提交本任务范围内的源码、测试、规范和发布说明为 `e388b5e`；推送 `main`、`v1.5.12`，远端 `.github/workflows/release.yaml` 构建与 Release 作业均成功，回读正文和 `AALC_v1.5.12.7z` 资产（工作流 `36223882455`）。实机未验收，任务保持 active 而不归档；正式版注明这一限制。

## 风险门槛

不触碰已安装可执行文件、用户配置、存档；不调用可能拖动队伍条目的手势。用户已授权发布但未授权操作当前运行游戏：实机测试另行征得同意，并确认进程及可用窗口，不能消耗正在挂机的游戏资源。出现连续三次同类无效尝试停止盲试，记录结果并请求所需实机条件。
