# 实施与集成检查

- [x] 启动两个子任务前复核对应 PRD 与规范；先完成归顶误判 RED→GREEN，保存真实坐标回归输出。
- [x] 选队子任务：测试真实截图坐标及跨比例、标题/缺行反例；最小修改 `tasks/team_list.py`；跑解析和选队测试、Ruff。
- [x] 上游子任务：在仅有已知选队改动的工作树中合并 `upstream/main@ddc2204` 保留祖先；审查图像和 `module/automation/automation.py` 自动合并，测试空输入防护及本地恢复/缓存契约。
- [x] 父任务：合并后复跑 `.venv/Scripts/python.exe -m pytest tests -q`（314 passed）、受影响文件 Ruff、`compileall`、`git diff --check`；`git merge-base --is-ancestor upstream/main HEAD` 成功，无未解决冲突。实机滚轮和季节领取不属于离线验证结论。
- [x] 已获用户实施及一次性提交批准，`4d7718c` 保留双父历史，规范与变更记录已更新；不推送/发布。
- [x] 两个子任务已归档，父任务最终检查完成；09-05、09-13 依用户实机反馈关闭，保留未能独立复现的分支和历史 ONNX 崩溃限制。父任务随任务记录一并归档提交。

高风险点：上游同一 `Automation` 文件的新防护虽然无文本冲突，仍需确认缓存的缺模板结果不会遮蔽资源同步后的加载，且未恢复上游旧的强制结束游戏逻辑。任何超出当前两文件的上游变化重新规划。
