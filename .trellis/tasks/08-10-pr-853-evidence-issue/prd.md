# PR #853 evidence and issue draft

## Goal

从 PR #853 中筛出**除 #827 已由 PR #854 覆盖的纽本入口阈值问题以外**、在昨晚实机测试稳定复现且已存在于上游基线的缺陷，为其建立可核验的证据并准备事实性 Issue 草稿；不修改产品代码，也不混淆 `main` 与 `pr/recovery-hardening`。

## Requirements

- 以 `pr/recovery-hardening`（干净 worktree：`E:/vsCode/Programs/AhabAssistantLimbusCompany-pr-recovery-hardening`）为唯一 PR 证据来源；不得将当前 `main` 的发布工作流提交混入 PR #853 的产品修复范围。
- 读取上游 PR #853、Issue #827 和 PR #854 的标题、diff、关闭/评论信息；明确排除已由 PR #854 覆盖的 `thread_enter_assets` 阈值问题，不能把它重述为新的 Issue。
- 将维护者提出的“无 Issue、无法复现、改动不关联”要求转化为可核验的 Issue 证据结构。
- 从本地实机日志、可用截图、回归测试与 PR 分支提交中提取可引用证据；已知复现并非偶发，Issue 必须陈述稳定的触发前置条件、实际行为、期望行为、日志时间段与回归验证。
- 对每个候选问题执行来源判定：分别对照上游 PR 基线、`pr/recovery-hardening` 的提交前后状态和对应实机日志；只有能证明在上游基线已存在且稳定复现的缺陷才作为上游 Issue 草稿。后续防御性增强、用户网络环境相关恢复或纯安全/性能加固必须明确排除，不能伪装为原项目 Bug。
- 按已完成来源判定的故障行为而非按文件或提交拆分 Issue；优先筛查昨晚实机复现的事件选项灰化、事件结果页推进/连续场次恢复、错误结算/失败传播等路径。只有每项证据足以独立复现时才单独成 Issue，不足时明确标为“不可主张的增强项”。
- 输出中文 Issue 草稿和英文简短版本（如上游 Issue 模板需要），保持事实和证据导向，不使用针对维护者的人身攻击语言。
- 不修改产品代码、`main` 或 `pr/recovery-hardening`；Issue 发布前由用户自行确认内容并在 GitHub 页面提交。

## Acceptance Criteria

- [x] 已记录 PR #853 的上游链接、PR 分支 `pr/recovery-hardening` 的 HEAD、相对上游基线 `b7f1d786` 的范围，以及当前 `main` 与该分支的明确隔离说明（见 `issue-evidence/pr-853/README.md` 第 0 节）。
- [x] 已单独记录并排除 #827/PR #854 覆盖的纽本入口阈值问题；不将其计入新 Issue（见 `issue-evidence/pr-853/README.md` 第 1 节）。
- [x] 已完成来源判定表：判定结果页不推进的实机模板块与上游基线逐字节一致；入口失败后继续选队在上游和实机版本均缺少失败门控（实机版本另有不相关日常改动，已在报告中明确）；灰化首项、服务器错误、Steam 与性能项均明确排除（见 `issue-evidence/pr-853/README.md` 第 2 节）。
- [x] 已为两份拟议 Issue 给出复现步骤、实际/期望行为、日志、基线代码与最小修复方向（见 `issue-evidence/pr-853/README.md` 第 3–4 节）。
- [x] 已明确已保留的日志/元数据/评论附件，以及缺失的两张原始游戏截图；未把无法取得的截图列为可上传附件（见 `issue-evidence/pr-853/README.md` 第 5 节）。
- [x] 已生成中文与英文短版 Issue 草稿，并说明拆分边界（见 `issue-evidence/pr-853/README.md` 第 3–4、6 节）。
- [x] 输出仅为证据归档和草稿；未创建 Issue、未更新远程分支、未修改产品代码。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
