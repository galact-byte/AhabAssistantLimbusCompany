# 主会话最终复核

## 实施边界
用户要求不再使用子代理后，后续停止生命周期实现、先前事件/恢复差异检查和全量验证均由主会话直接执行。没有改G盘运行目录、用户配置或游戏进度，没有提交/发布。

## 新鲜验证
- `.venv/Scripts/python.exe -m pytest tests -q`：259 passed in 10.02s，`main-full-tests.txt`。
- `.venv/Scripts/python.exe tests/native_stop_probe.py`：真实QThread和现有RapidOCR ONNX引擎，3次推理中重复请求停止、3次随后正常启动完成；全部断言成立，子进程退出码0，`native-stop-probe.txt`。输入为合成文字图片，不是游戏证据截图。
- `.venv/Scripts/python.exe -m compileall -q app module tasks tests`：退出码0。
- `git diff --check`：退出码0，只有Git换行转换提示。
- Ruff逐文件对HEAD比较（28个变更Python文件，ignore E722）：新增0，遗留67。保存于`main-lint-comparison.json`，不宣称全库lint无告警。

## 复核重点
- 事件结果期限独立于整场战斗，重复点击不能刷新；成功/失败与SKIP/继续坐标约束、正常动画、服务器错误优先有回归。
- 恢复锁覆盖关闭到主页确认，截图底层/监控不重启；镜牢False按新帧落点分流，不等同战败；入口失败传播。
- 取消不直接打断原生调用；监控收到停止请求并可从暂停输入退出，真实join后清缓存。业务普通异常处理不会吞TaskCancelled；历史裸except可能延迟传播，下一共享截图/输入边界再次检查。
- 手动停止不提前开放启动/设置；关闭确认后轮询保持Qt线程对象存活；Qt finished才执行UI清理及退出。
- 完成哨兵仍为True且使用身份比较，但仅记录exit_requested，不再由未退出线程发送kill_signal；False/None不退出。
- 补充RED：监控暂停阻塞、完成边界收到取消、提前销毁窗口；失败输出分别保存，没有拿修改后的测试假装历史合同未变。

## 尚未验证与风险
- 未读到历史WER dump，真实隔离测试通过不证明历史访问冲突已根治。
- 原生调用永久挂起时协作停止不能强制结束，UI保持等待；推理进程隔离未获新架构批准，未实施。
- 未打包、未部署G盘、未跑真实游戏/Steam/模拟器/无人值守长测。工具页自身工作线程不是本次主任务线程，未扩展重构其生命周期。
- 上游归属仅核对本地提交与Issues缓存，未实时联网核验，不生成外部缺陷报告。

## 交付状态
源码和可用本地验证已完成，任务保留in_progress等待外部验收/后续交付指令，不冒充已部署或整体验收完成。
