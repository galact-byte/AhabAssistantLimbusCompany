# 恢复修复栈 PR 准备实施计划

## 目标

从当前 30 提交恢复修复栈创建无未跟踪文件污染的 `pr/recovery-hardening` 分支，完成审查和验证后推送；用户使用 Compare URL 自行创建 PR。

## Task 1：创建隔离 PR worktree

- [ ] 记录原工作区分支、HEAD、未跟踪文件和 `origin/main` 共同祖先。
- [ ] 确认新分支不存在且 sibling worktree 路径不存在。
- [ ] 执行 `git worktree add -b pr/recovery-hardening <sibling-path> ee9a86c`。
- [ ] 在 sibling worktree 运行 `git status --short`，预期无输出；运行 `git log --oneline $(git merge-base origin/main HEAD)..HEAD`，预期 30 个恢复提交。

## Task 2：双轴审查

- [ ] 运行规范审查：检查 `origin/main...HEAD` 的 diff 与 `.trellis/spec/backend/{error-handling,quality-guidelines,logging-guidelines}.md`。
- [ ] 运行需求审查：检查恢复任务 PRD/设计/实现计划所需的服务器错误、日常状态机、Steam 云同步恢复和测试覆盖。
- [ ] 只修复有代码/测试证据的问题；每个修复增加或调整回归测试、运行失败测试确认 Red 后再实现 Green。
- [ ] 记录审查结论；若没有确认问题，不修改产品代码。

## Task 3：在干净分支验证

- [ ] 运行 `uv run pytest`，必须为零失败。
- [ ] 运行受影响模块和测试的 Ruff 命令，必须为零新增 lint 失败。
- [ ] 运行 Python `compileall` 与 `git diff --check origin/main...HEAD`。
- [ ] 确认 `git status --short` 只有经过审查的已提交变更，最终干净。

## Task 4：推送与人工 PR 交接

- [ ] 用 `git push --set-upstream origin pr/recovery-hardening` 推送新分支；不推送当前开发分支。
- [ ] 读取 `git ls-remote --heads origin pr/recovery-hardening` 确认远程 ref 指向预期提交。
- [ ] 输出 Compare URL、推荐 PR 标题和基于已验证内容的说明要点。
- [ ] 明确用户在 GitHub 页面点击 **Create pull request** 并自行提交；不调用 `gh pr create`。

## 风险与回滚

- 原工作区的未跟踪 `.trellis` 文件不是 PR 输入；任何出现在新 worktree 的未跟踪文件都是停止信号，需先清理原因。
- 若审查发现跨模块问题，修复只落在 `pr/recovery-hardening`，不改原分支。
- 不执行 `push --force`、不删除远程分支、不自动创建 PR。
