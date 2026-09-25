# 修改记录 — Ahab Assistant Limbus Company

## 2026-09-25 — 编队归顶误判修复与上游 main 融合（未游戏实机验证）

### 背景与结果
- 两次 v1.5.10 经验本选队失败截图中，“编队”标题下沿 y=371、“剧情关卡”上沿 y=377，比例 0.625；旧 `12 * scale` 门限误排首项。`tasks/team_list.py` 调为 `6 * scale`，仍拒绝与标题重叠或列表缺行的输入；未改变滚轮和按顺序/编号选队语义。
- 融合 `KIYI671/AhabAssistantLimbusCompany` 上游 `main@ddc2204` 的五个祖先提交：季节入口图片及 `Automation.find_feature_element` 对缺模板、无截图、空裁剪的保护。资源同步后 `clear_img_cache()` 同时清普通缓存和缺模板标记，本地彩色帧、OCR、恢复及停止逻辑保留。

### 文件与兼容性
- 修改 `tasks/team_list.py`、`module/automation/automation.py`、`assets/images/default/share/home/season_assets.png`；新增/更新 `tests/test_feature_matching_input_guards.py` 与 `tests/test_team_list_parser.py`。
- 无新依赖、配置迁移、用户数据变更；未修改 G 盘运行目录或推送/发布。回滚需审查本次归顶改动及上游合并提交，不能覆盖其他本地改动。

### 验证与限制
- 两张原始失败 PNG 经现有 OCR 与解析流程重放，均以“剧情关卡”为首行、判定归顶；归顶修复先红后绿。上游输入保护四项先红，合并后转绿，另测缺模板缓存清理后重新匹配。
- `.venv/Scripts/python.exe -m pytest tests -q`：314 passed；受影响文件与测试 Ruff（既有 E722 豁免）、compileall、差异空白检查通过。
- 未在游戏中验证编队滚轮、队伍最终选中或季节领取；不能把离线测试当作 G 盘安装版已更新或实机验收。

## v1.5.10 — 编队安全滚动与选后校验（未游戏实机验证）

### 背景与目标
- Windows 编队列表不再按住左键拖动，避免触发游戏支持的长按重排；不宣称复现了历史移队过程。
- 按顺序以实际第 N 项为目标（第二项可以是编队#3），按编号精确匹配；成功必须有顶部当前编队标题证据。

### 文件与兼容性
- `module/automation/input_handlers/input.py`：前台/后台编队滚动专用滚轮、列表客户端坐标转屏幕坐标、暂停检查与 finally 恢复鼠标；window_move 明确失败，不回退拖动。普通地图滚轮不变。
- `tasks/team_list.py`：纯 OCR 列表/标题分区、缺行与重名拒绝、页间重叠拼接。
- `tasks/teams/team_formation.py`：观察归顶并下滚/回顶验证输入生效、按需扫描至目标、当前画面定位、最多3次选后校验；截图/识别/无进展有限失败，保存可用失败画面到 `logs/team-selection-failed-*.png`。模拟器仍调用原专用触摸手势。
- 新增 `tests/test_team_{safe_input,visual_selection,list_parser}.py`；复用镜牢和日常失败传播边界。未修改配置、人格、编队码或发行目录。
- 回滚只需还原上述产品代码，不涉及数据迁移；新测试与本条记录随变更处理。

### 验证与限制
- 主会话独立复验 `.venv/Scripts/python.exe -m pytest tests -q`：307 passed；触及产品文件及全部 tests 的 Ruff（既有 E722 豁免）通过。主会话另补4项RED，纠正全量扫描带来的多余操作和非40槽失败。
- RED 原实现17项失败；额外 OCR 异常与首页提示回归分别保存 RED 证据。记录位于任务 `research/`。
- 用户提供的左侧裁剪截图已用现有真实 OCR 离线验证前三项为剧情关卡、编队#3、编队#4；缺少完整页面定位与标题，不能替代1600×900后台实机验收。
- 已移除每次扫描40槽的限制：按顺序只扫描到目标，按编号当前页可定位则不滚动；第二项位于顶部时通过不超过8次滚轮操作的回归（被替换的全量扫描实现为67次）。只检查经过页面的重复/歧义，不扫描无关远端队伍。归顶无法验证滚动生效、无法完整识别或页间无重叠时保守失败。未发送真实游戏输入，实际滚轮响应、完整页面几何、模拟器与长时间运行待验证。

## v1.5.9 — 事件结果页、镜牢恢复链与协作停止（未游戏实机验证）

### 背景与目标
- v1.5.8 日志证实结果页约15分钟不推进、重启后主页空转与ONNX原生闪退；修复前两条链及停止时强杀线程的风险，不宣称历史闪退已根治。

### 影响与实现
- `tasks/event_page.py`、`tasks/battle/battle.py`、`tasks/base/back_init_menu.py`：结果上下文/几何约束的继续与SKIP识别，独立60秒期限，重复点击不刷新期限；不全局降低模板阈值。
- `tasks/base/retry.py`、`module/automation/{automation,screenshot}.py`：重启所有权覆盖关闭、启动和主页确认；底层/监控截图不自行启动，业务持续截图失败在锁外请求恢复；禁止恢复内嵌套重启。
- `tasks/mirror/mirror.py`、新增 `tasks/base/home_page.py`：False按地图/主页/未知落点恢复，主页导航OCR辅助与有界重进入口，修正搜索模式被重置。
- 新增 `tests/test_{event_result_progress,home_navigation,runtime_recovery}.py`，更新日常事件、服务器错误及Steam恢复测试合同。
- 新增 `module/task_control.py`，修改脚本/监控线程、OCR/截图/输入边界及 `app/{farming_interface,my_app}.py`：协作取消替代强杀，监控真实join后清缓存，Qt finished后允许再次启动；退出意图延后、关闭等待安全退出。覆盖暂停及维护等待、取消不执行完成动作。
- 未更改运行目录、用户配置或游戏数据。事件、恢复链、生命周期应分别回滚，禁止整库覆盖还原。

### 验证与限制
- `.venv/Scripts/python.exe -m pytest tests -q`：259 passed in 10.02s（原208）。主会话全量输出在任务 `research/main-full-tests.txt`。
- `tests/native_stop_probe.py`：隔离进程真实Qt/ONNX六轮，3次推理中重复停止、3次随后正常任务，全部断言通过且退出码0；使用合成图，不操作游戏。
- compileall、`git diff --check`通过；28个变更Python文件Ruff对HEAD比较无新增诊断（排除既有E722），仍有67条既有诊断，不宣称全库lint全绿。见 `research/main-lint-comparison.json`。
- 未打包/部署/游戏实机验证；真实SKIP、Steam/模拟器及长时间无人值守仍待验收。没有历史原生dump，不能证明闪退最终触发机制；原生调用永久不返回时仍等待安全结束，不擅自引入进程隔离。

## 2026-09-12 — 上游融合与商店、主题包卡顿修复

### 背景与目标
- 融合上游 `41299bb`，保留本地命名编队、事件恢复、地图门闩及失败不退出保护；双父合并提交 `eb4d83d` 已落地，未发布。
- 修复离店点击命中绕过重试预算的问题，加入弹窗优先与失败传播。
- 补齐剩余战斗力 OCR 的10–12人总数候选，避免合法的 `5/12` 等被遗漏。

### 影响与兼容性
- 接入上游40队、模拟器连接、寻路及困难层切换等改动；未安装依赖、未修改运行目录或用户配置。
- 商店恢复失败交由镜牢任务错误边界处理，不伪报正常离店。
- 该次双父合并已提交，后续回滚须审查合并提交与用户改动，禁止直接清理工作区。

### 文件与实现
| 操作 | 路径 | 说明 |
|---|---|---|
| 修改 | `tasks/mirror/in_shop.py`、`shop_presence.py`、`mirror.py` | 有界离店、纯 OCR 弹窗识别及恢复失败传播。 |
| 修改 | `tasks/teams/team_formation.py` | 融合40队与本地匹配，补齐存活人数范围。 |
| 新增 | `tests/test_shop_leave_*.py`、`test_mirror_shop_failure.py`、`test_team_survival_count.py` | 离店及人数回归。 |
| 新增 | `tests/test_mirror_route_weights.py`、`test_retry_monitor_lifecycle.py` | 寻路权重与监视器点击门检查。 |

### 验证
- `uv run --no-sync pytest -q`：208 passed，9.23秒。新增主题包截图/识别异常预算及失败传播回归。
- 聚焦 Ruff、compileall 与 `git diff --check HEAD`：通过。
- 全受影响文件 Ruff：312项，双方基线对照未新增诊断；不能宣称全库 lint 全绿。

### 已知限制与后续
- 尚未打包或实机验证；商店模板失配的像素原因未确定。
- 209条开放 Issue 已完成正文及模块聚类适用性分类；环境或证据不足的未宣称不存在，不包含全附件实机复现。
- 主题包截图失败、识别异常绕过预算的问题已修复，恢复失败不再继续记录楼层进度。
- 本地集成检查已完成，双父合并提交 `eb4d83d` 保留上游历史；未发布。

## 2026-08-10 — 发布与镜像同步改为显式操作

### 背景与目标
- 普通 `main` 推送会意外进入预发布与 MirrorChyan 同步链路；正式 GitHub Release 也会自动触发 MirrorChyan 工作流，导致不必要的发布尝试和失败记录。
- 现将预发布和 MirrorChyan 同步改为明确的手动动作，保留普通 CI 的测试与构建。

### 影响与兼容性
- 普通 `main` 推送不会触发 CI、构建或任何发布；PR 和未勾选发布选项的手动 CI 运行只测试与构建，绝不会创建 GitHub Release、预发布标签或启动 MirrorChyan 工作流。
- 需要预发布时，在 `CI Build` 的 **Run workflow** 中仅从 `main` 执行，并显式勾选“创建预发布 Release”。
- MirrorChyan 安装包和说明同步只能分别从其工作流的 **Run workflow** 手动执行；两者均改为读取当前 `galact-byte/AhabAssistantLimbusCompany` 仓库的 Release。

### 文件与实现
| 操作 | 路径 | 说明 |
|---|---|---|
| 修改 | `.github/workflows/ci.yaml` | 预发布改为手动布尔开关，移除自动 MirrorChyan 调度并收紧权限。 |
| 修改 | `.github/workflows/release.yaml` | 保留标签正式发布，移除自动 MirrorChyan 调度并收紧权限。 |
| 修改 | `.github/workflows/mirrorchyan_release.yml` | 将安装包同步来源改为当前仓库，保持手动触发。 |
| 修改 | `.github/workflows/mirrorchyan_release_note.yml` | 移除 Release 编辑事件触发，说明同步改为手动触发，并改为当前仓库来源。 |

### 验证
- 工作流 YAML 解析与触发条件断言：通过，确认 `main` 推送无法发布预发布或调度 MirrorChyan。
- `uv run pytest -ra`：133 passed。
- `git diff --check`：通过。

### 已知限制与后续
- MirrorChyan 的实际手动同步仍依赖有效的 `MirrorChyanUploadToken` 和 `AALC` 资源授权；首次手动同步时需在 Actions 日志确认其配置。


## 2026-08-09 — Steam 云同步无人值守启动恢复

### 背景与目标
- Steam 云同步失败确认会阻断《边狱巴士》启动；旧逻辑在找不到游戏窗口时会无限重复调用 Steam，且多个恢复入口直接强杀游戏，容易加剧未同步退出。
- 现改为有界的单次启动请求：仅精确识别用户授权的“无法同步 → 仍然进行游戏”中文弹窗后自动继续，避免夜间挂机卡住。

### 影响与兼容性
- Windows 非模拟器路径新增 Steam 桌面弹窗 OCR 处理，不新增依赖、无配置或存档迁移。
- 只会点击完整同区域中文签名中的“仍然进行游戏”；不会点击“取消”或其他 Steam 控件。实际 Steam/网络云同步故障仍由 Steam 处理。
- 游戏关闭改为优先发送 `WM_CLOSE` 并等待 30 秒，超时后才使用集中式 `taskkill /F /IM LimbusCompany.exe` 兜底；模拟器路径不变。
- 可回滚本条变更涉及的模块；回滚会恢复旧的强杀与无限启动重试行为，不建议作为常规处理方式。

### 文件与实现
| 操作 | 路径 | 说明 |
|---|---|---|
| 新增 | `module/game_and_screen/steam_cloud.py` | 纯 OCR 弹窗解析与延迟导入的桌面截图/OCR/点击适配器。 |
| 修改 | `module/game_and_screen/game.py` | 单次待启动状态、云同步一次确认、精确进程名识别与优雅关闭。 |
| 修改 | `module/game_and_screen/screen.py` | 支持仅检查窗口、禁止启动轮询隐式重开 Steam。 |
| 修改 | `tasks/base/script_task_scheme.py` | 120 秒单调时钟启动上限和明确的窗口启动失败出口。 |
| 修改 | `tasks/base/retry.py`、`module/system_actions.py`、`module/automation/{automation,screenshot}.py` | 所有 Windows 关闭/重启入口委托公共优雅关闭逻辑。 |
| 新增 | `tests/test_steam_cloud_recovery.py` | 覆盖同窗识别、点击安全、启动状态、关闭策略和调用方收敛。 |
| 修改 | `tests/test_daily_team_selection.py` | 隔离与本断言无关的真实截图/窗口调用，避免顶层任务测试访问本机 Steam/进程。 |
| 修改 | `.trellis/spec/backend/{error-handling,quality-guidelines}.md` | 记录有界启动、桌面弹窗授权和公共退出契约。 |

### 验证
- `uv run pytest`：128 passed。
- `uv run ruff check module/game_and_screen/steam_cloud.py module/game_and_screen/game.py module/game_and_screen/screen.py module/automation/automation.py module/automation/screenshot.py tasks/base/retry.py tasks/base/script_task_scheme.py module/system_actions.py tests/test_steam_cloud_recovery.py tests/test_server_error_recovery.py tests/test_daily_team_selection.py --ignore E722`：通过。
- `python -m compileall module/game_and_screen module/automation tasks/base module/system_actions.py`：通过。
- `git diff --check`：通过。

### 已知限制与后续
- Steam 弹窗的实际桌面端到端确认仍需用户在真实“无法同步”场景中验证；自动化测试已覆盖截图对应的 OCR 布局和安全拒绝分支。

## 2026-08-08 — 日常战斗事件状态机与恢复栅栏

### 背景与目标
- 日常连续场次不再每场回主界面后，纽本判定结果页可能残留；旧模板在 beta 截图上无法识别“继续”，下一场会错误地在事件页寻找纽本入口。
- 新增通用 OCR 事件页解析、事件结果动画等待、主页恢复和日常入口的一次性恢复，避免按单个事件文案堆叠模板补丁。

### 影响与兼容性
- 涉及战斗事件、返回主界面和经验本/纽本入口恢复；不新增依赖、不修改用户配置，也不取消“同项目连续场次不回主页、项目结束后统一换饼”的现有行为。
- 事件选项页以**首项按钮的灰化状态**决定目标：首项灰化才点次项；首项可用时始终重试首项，绝不会仅因页面仍存在就改点次项。OCR 缺失、没有替代项或重复点击未推进时，经过有界重试后终止当前战斗，不会等待到总战斗超时。
- `tasks.event.event_handling` 继续重导出事件解析接口，`from tasks.event import event_handling` 仍返回原有 `EventHandling` 单例。
- 可按本次 5 个提交分别回滚；不需要数据迁移。

### 文件与实现
| 操作 | 路径 | 说明 |
|---|---|---|
| 新增 | `tasks/event_page.py` | 无运行时 OCR/自动化依赖的纯 OCR 事件页解析器。 |
| 修改 | `tasks/event/event_handling.py` | 重导出解析接口，保留既有判定对象选择行为。 |
| 修改 | `tasks/battle/battle.py` | 模板推进失败时以 OCR 处理事件“继续/进行判定”，结果动画期间重置局部识别机会而不重置战斗总超时；灰化首选项切换、可用首项 OCR 回退与有界选项重试。 |
| 修改 | `tasks/base/back_init_menu.py` | 返回主页前推进或有界等待事件结果页；最长等待 60 秒。 |
| 修改 | `tasks/daily/luxcavation.py` | 经验本/纽本入口耗尽后最多执行一次**禁用内部重启**的主页恢复并完整重试；续费恢复或服务器错误失败后立即停止当前入口。 |
| 新增 | `tests/test_daily_event_recovery.py` | 覆盖 OCR 解析、灰化选项选择、战斗等待、主页恢复、入口恢复和有界选项重试。 |
| 修改 | `tests/test_daily_team_selection.py` | 覆盖战斗、主页恢复和日常组失败向上层批次/顶层任务的终止传播。 |
| 修改 | `tests/test_server_error_recovery.py` | 覆盖战斗、经验本和纽本对服务器错误“终止/跳过/继续”三态的优先处理。 |
| 新增 | `tests/test_event_import_compatibility.py` | 锁定事件包的原有单例导入契约。 |

### 验证
- `uv run pytest`：105 passed；覆盖事件结果“继续”、结果动画等待、60 秒上限、40 秒后按钮出现、主页恢复、入口一次恢复、服务器错误三态优先级、首项灰化选择、不同分辨率候选槽位、选项页有界退出与顶层失败硬门。
- `uv run ruff check tasks/battle/battle.py tasks/event_page.py tasks/event/event_handling.py tasks/base/back_init_menu.py tasks/daily/luxcavation.py tasks/base/script_task_scheme.py tests --ignore E722`：通过；`E722` 为既有基线豁免。
- `git diff --check`：通过。

### 已知限制与后续
- 自动化测试已通过，但尚未完成真实游戏中的“纽本多场 + 判定事件”端到端回归；在该实机验证前，不能宣称问题已在 beta 游戏界面修复。
- 实机验收应保持已知配置：`select_team_by_order: true`、`daily_task: true`、`set_EXP_count: 1`、`set_thread_count: 3`、`daily_teams: 1`；重点观察首项不可用（灰色）时直接选择第二项、首项可用时绝不跳项、约 40 秒结果动画、OCR 点击继续和下一场正常进入纽本。
