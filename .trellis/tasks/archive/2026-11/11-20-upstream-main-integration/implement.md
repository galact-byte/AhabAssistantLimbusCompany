# 执行与验证

- [x] 检查用户授权、仓库状态、远端与上游提交。
- [x] 读取项目工作流、质量与运行恢复规范。
- [x] 运行基线：`.venv/Scripts/python.exe -m pytest -q`，322 passed。
- [x] 执行 `git merge --no-commit --no-ff ec8aa17` 并逐块融合冲突。
- [x] 全量 pytest，333 passed；检查本地行为及上游新功能接口兼容。
- [x] 运行受影响 Python 文件 Ruff、语法和 `git diff --check`；36个文件与两份基线对比无新增 Ruff 诊断。
- [x] 更新 CHANGES.md、质量规范及 `research/` 验证记录；真实 Qt/ONNX 六轮通过。
- [x] 创建双父融合提交 `05f39ee`；验证后归档本任务。
- [x] 推送 origin/main，远端回读为 `05f39ee207ec6a4dd128881505a6c63d8a3ec29f`。归档与会话记录另行提交推送并复核。

## 审查重点
编队滚动与确认失败传播、事件动画期限、重启所有权、停止生命周期、资源缓存更新、奖励配置向后兼容。不得用模拟测试宣称游戏实机通过。
