# 事件与运行恢复合同

## 1. 范围与触发
适用于结果页长等待、业务与监控截图失败、镜牢战斗返回主页。停止生命周期见下节；不能用Python锁或隔离压测成功声称历史ONNX崩溃已根治。

## 2. 签名
- `resolve_event_page(entries) -> EventPageResolution | None`；`EVENT_RESULT_TIMEOUT = 60.0`。
- `restart_game(*, close_first=False) -> bool`。
- `back_init_menu(*, allow_restart=True)`；恢复拥有者必须传False。
- `find_home_drive(entries) -> tuple[int, int] | None`。

## 3. 数据与返回合同
- 结果上下文只接受完整“判定成功/判定失败”，推进按钮完整“继续/SKIP”且在结果下方/右侧，继续优先；不修改全局模板阈值。
- 60秒从结果首次出现起算，OCR/模板反复点击不能重置。离开结果页才重置；40秒正常动画保留。
- 重启拥有者的非阻塞锁包含close/init/主页确认，嵌套False不执行关闭；成功True仅代表主页已确认，失败抛cannotOperateGameError；finally释放锁。
- 底层/监控截图None不触发重启。业务跨调用60秒失败在截图锁外申请恢复；retry在拥有者恢复中60秒无图须报错，不能无限重入。
- 镜牢battle False需新帧落点识别：地图继续，主页road_to_mir，未知有界back_init_menu后最多一次重启；不能一律视战败，也不能丢弃False。
- 主页OCR同时要求同一行、玻璃窗在驾驶席左侧；检测和点击复用find_home_drive。入口每轮均消耗预算，失败False由调用者抛任务错误。

## 4. 校验与错误矩阵
| 输入 | 结果 |
| --- | --- |
| 仅SKIP/剧情包含继续/按钮几何错误 | 不授权OCR推进 |
| 正常40秒结果动画 | 等待后继续 |
| 60秒结果重复不变（即使每次点击命中） | False并由调用者恢复 |
| 嵌套restart_game | False，无close/init |
| 启动失败/不能确认主页 | 异常并释放锁 |
| 地图上battle False | 不回主页、不重启 |
| 主页模板失败但双导航OCR成立 | 实际点击驾驶席后重进 |
| 入口持续无图/点击却不前进 | 预算耗尽False |

## 5. 正常、基础与错误示例
- 正常：弹窗优先处理，结果40秒后出现继续并切回战斗。
- 基础：战斗超时已经重启到主页，镜牢直接重进，不再第二次回主页。
- 错误：监控截图无窗口便自行close/init，会与业务启动交叠。

## 6. 必须测试
`test_event_result_progress.py`、`test_home_navigation.py`、`test_runtime_recovery.py`及既有日常/Steam/服务器错误回归。断言点击位置、时间上界、重启次数、锁外恢复、异常锁释放与False传播。真实按钮/原生崩溃需要实机证据，mock不替代。

## 停止生命周期合同
- `cancellation_scope(Event)` 仅绑定当前线程；`checkpoint()` / `sleep(seconds)` 在安全边界抛 `TaskCancelled(BaseException)`，不能被普通业务 `except Exception` 吞掉。
- `my_script_task.terminate()` 仅设置业务和监控停止事件，不调用Qt原生terminate、不更换锁、不在UI线程join。OCR返回、截图和输入入口检查取消；暂停等待及维护/启动等待可取消。
- `run()` finally必须等待监控实际join，然后清缓存。`QThread.finished` 才允许UI恢复启动/配置；退出哨兵仅记录 `exit_requested`，完成槽走窗口close而非直接sys.exit。
- 关窗确认后保持事件循环，100ms轮询等待工作线程退出，不重复弹确认框。原生调用永不返回时仍会保持“正在停止”，不能硬杀来伪装成功；进程隔离属另行评审范围。
- 正常：推理返回后取消、不执行下一输入；基础：重复停止幂等，下一次新建worker正常运行；错误：停止按钮提前解锁或monitor.join(2)后丢失活线程引用。
- 必须测试：`test_cooperative_stop.py`、`test_stop_ui_lifecycle.py`、`test_script_task_exit_signal.py`。`tests/native_stop_probe.py` 在隔离进程使用合成图验证真实Qt/ONNX停止与再次启动，不替代游戏实机和历史dump。

## 7. 错误与正确写法
- 错误：点击成功即重置等待期限；正确：只在结果页消失时重置。
- 错误：`kill_game(); restart_game()`分散恢复所有权；正确：`restart_game(close_first=True)`覆盖关闭与启动。
- 错误：`main_loop_count >= 50`便设clam；正确：每轮按`<15 aggressive / <75 normal / 其余clam`，避免50–74区间覆盖normal。
