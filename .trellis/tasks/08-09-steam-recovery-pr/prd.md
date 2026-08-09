# 审查恢复修复并准备纯净 PR

## Goal

将当前 `fix/daily-team-selection-guard` 相对 `origin/main` 的完整恢复修复栈（31 个提交，含一个已归档 Trellis 任务的 bookkeeping 提交）在隔离且无未跟踪文件污染的 worktree 中审查、验证，并推送为一个可提交至 `galact-byte/AhabAssistantLimbusCompany` 的 PR 分支。

## Background

当前分支相对 `origin/main` 的共同祖先 `c8763279453725185ead9c4c035dc2f9244441fa` 包含 31 个提交、48 个文件，覆盖：服务器错误弹窗恢复、队伍名称和自定义字体编号识别、日常批次导航、日常事件状态机、Steam 云同步无人值守启动恢复，以及对应测试、规范与变更记录。第 31 个提交 `ee9a86c` 仅归档 Steam 恢复任务，保留它使 PR 与候选头一致。

用户选择推荐范围：提交整个关联修复栈，而不是仅切取 Steam 修复的 3 个提交。原因是日常和 Steam 恢复共同依赖启动、关闭、错误出口及回归测试；拆分会留下难以独立验证的上下文。

原工作区有未跟踪的 Trellis 初始化/运行文件。项目 `.trellis/.gitignore` 明确忽略 `.developer`、`.current-task`、`.runtime/`、`.agents/`、`.agent-log`、`.session-id`、`.plan-log`、`*.tmp`、`.backup-*`、`*.new` 及 Python 缓存；项目全局规范建议追踪工作流、spec、任务和开发者 workspace 等协作资产。此 PR 使用干净 worktree，只基于提交历史，不携带原工作区任何未跟踪文件。

当前环境没有 `gh` CLI；可以推送 Git 分支，但不能通过 GitHub CLI 自动创建 PR。

## Requirements

### R1 范围与纯净隔离

从 `origin/main` 的共同祖先创建新的 PR 分支，包含当前恢复栈的全部 30 个提交；在新的 Git worktree 中操作，分支工作区必须没有原工作区未跟踪文件。

### R2 双轴审查

对 `origin/main...PR 分支` 执行独立的规范审查与需求/行为审查。所有确认的 P1/P2 问题必须修复并重新验证；没有确认的问题则记录审查结论。

### R3 验证

在干净 worktree 中运行完整 `uv run pytest`、受影响文件 Ruff 检查、`compileall` 和 `git diff --check`。验证失败不得推送。

### R4 推送与手动 PR 交接

使用显式的新远程分支名推送到 `origin`，不得推送当前开发分支或任何未跟踪文件。用户自行在 GitHub 网页创建并提交 PR；交接必须输出 GitHub 比较/新建 PR URL 和最短网页操作步骤。不得尝试自动创建远程 PR。

## Out of Scope

- 不在本任务中添加新的产品功能或进行无关重构。
- 不把原工作区未跟踪的 Trellis 初始化文件纳入 PR。
- 不强制提交尚处于实机验收中的日常任务之外的用户本地工作。
- 不推送当前 `fix/daily-team-selection-guard` 分支。

## Acceptance Criteria

- [x] 新 PR 分支以 `origin/main` 为基线，包含当前恢复修复栈，且 worktree 无原工作区未跟踪文件。
- [x] 双轴审查完成；确认的 Steam 桌面点击安全问题已修复，无遗留确认的 P1/P2 问题。
- [x] 干净 worktree 的全量 pytest、Ruff、compileall、diff 检查均通过。
- [x] 仅 PR 分支被推送至 `origin`，输出可打开的 GitHub 比较/新建 PR URL 和手动创建步骤。
- [x] 原分支和其未跟踪 Trellis 文件保持未改动。

## Verification Evidence

- 纯净 worktree：`E:/vsCode/Programs/AhabAssistantLimbusCompany-pr-recovery-hardening`，创建后与推送后 `git status --short` 均为空。
- 分支：`pr/recovery-hardening`；相对 `origin/main` 最终为 34 个提交（完整原恢复栈 31 个，含 `ee9a86c` 任务归档提交；审查新增 3 个 Steam 桌面点击安全修复提交）。
- 审查确认并修复：精确标题/取消按钮布局、前台 Steam 窗口范围 OCR、OCR 后点击前前台窗口重验证。
- `uv run pytest`：131 passed。
- 受影响代码与全部测试的 Ruff：通过；`python -m compileall module tasks`：通过；`git diff --check origin/main...HEAD`：通过。
- 推送回读：`origin/pr/recovery-hardening` 与本地 HEAD 同为 `9fc8af5bdafa845a435dd1261283a1aa84bb135b`。

## Open Questions

无。用户已决定提交完整关联修复栈，并明确要求创建纯净分支后推送。
