# 实施步骤

- [x] 读取项目 backend 规范、TDD 与 change-log 指引；核对 `upstream/main` 仍为 `ddc2204`，工作区仅有 Trellis 未跟踪目录和本轮已验证的选队改动。
- [x] 用当前 fork 上的现有测试检查模板缺失、空截图与空裁剪的旧行为；为缺失契约补 RED，保存失败证据。
- [x] `git merge --no-commit --no-ff upstream/main`；审查冲突与自动合并、图像资产和 `Automation` 本地不变量。
- [x] 资源同步已调用 `clear_img_cache()`；补充“缺失后可用”聚焦测试，通过缓存失效检查，无需额外产品改动。
- [x] 受影响测试、`.venv/Scripts/python.exe -m pytest tests -q`（314 passed）、Ruff、编译检查和历史祖先核对通过；结果交父任务复验，`4d7718c` 保留上游 `ddc2204` 祖先。

停止/回滚：出现冲突或行为差异先检查原代码和截图恢复，禁止 `git reset --hard`、`-X theirs`、覆盖 09-05/09-13 的目录及 G 盘运行目录；未经用户许可不推送或发布。
