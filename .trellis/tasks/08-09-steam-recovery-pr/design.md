# 恢复修复栈 PR 准备设计

## 分支与隔离

以当前提交 `ee9a86c` 为候选头、`origin/main` 为 PR 基线。创建新的本地分支 `pr/recovery-hardening`，并在项目外的 sibling worktree（`E:/vsCode/Programs/AhabAssistantLimbusCompany-pr-recovery-hardening`）检出。worktree 只从 Git 已提交对象创建，因此不会携带原工作区的未跟踪 `.trellis/` 文件。

不会修改或推送 `fix/daily-team-selection-guard`。推送时使用显式 refspec：

```bash
git push --set-upstream origin pr/recovery-hardening
```

## 审查模型

审查基线固定为 `origin/main...pr/recovery-hardening`，覆盖共同祖先之后的全部 30 个提交。执行两条独立轴：

1. **规范轴**：检查项目 backend Trellis 规范、全局项目规则与自动化状态机的有界恢复/测试约束；
2. **需求轴**：从当前恢复任务链的 PRD、设计、实现计划和提交范围，检查服务器错误、日常状态机、Steam 启动恢复是否遗漏、越界或行为错误。

确认问题才改动；修复必须在 PR worktree 中完成并提交到新分支。没有确认的问题也保留审查结论，不作猜测性重构。

## 验证模型

所有验证在 PR worktree 执行：

```bash
uv run pytest
uv run ruff check module tasks tests --ignore E722
python -m compileall module tasks
python -m compileall module/game_and_screen module/automation tasks/base module/system_actions.py
git diff --check origin/main...HEAD
```

如果 `module tasks` 的全范围 Ruff 受既有基线影响，则记录确切输出并至少运行已变更文件/测试的精确 Ruff 命令；本任务自身不接受新增 lint 失败。

## 手动 PR 交接

推送成功后生成：

```text
https://github.com/galact-byte/AhabAssistantLimbusCompany/compare/main...pr/recovery-hardening?expand=1
```

用户在该页面选择 **Create pull request**，填写基于已验证改动的标题和说明，再自行提交。当前环境没有 `gh`，本任务不调用 GitHub CLI 创建 PR。

## 回滚

推送前可直接删除本地 `pr/recovery-hardening` worktree 与分支，不影响原工作区。推送后若发现问题，可关闭 PR 或在同一 PR 分支追加修复提交；不重写历史、不强推。
