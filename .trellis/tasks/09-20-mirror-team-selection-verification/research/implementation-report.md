# 实现交接 — 2026-09-20

## 已实现
- Windows `mouse_swipe_for_team_scroll` 专用安全路径：前台定位后滚轮；后台 WM_MOUSEWHEEL 的 lParam 使用列表客户端点转换后的屏幕坐标，支持 PostMessage/SendMessage。dy 只取方向，每次一个刻度；普通 mouse_scroll 不变。
- 输入前 wait_pause、现有 Automation 交互门/锁继续包裹该接口；鼠标 finally 恢复；window_move 返回False，不拖动、不移动窗口。模拟器原专用触摸接口及实现文件未改。
- 纯解析 `tasks/team_list.py`：以橡皮擦模板坐标和列表标题几何圈定列表，按 y 排序自定义名称，行间距拒绝漏行，排除预设；标题证据仅来自顶部而非左侧目标文本。
- 选队先观察归顶，再通过相邻页面重叠遍历40槽，防止中途滚轮失效被误认为顶/底，并检测跨页重名；从底部按实际画面回找目标，不套旧像素/固定行坐标。按顺序与名称编号独立。未缓存跨轮位置。
- 读取最多3次、单阶段滚动最多100次、点击核验最多3次。失败返回False，写日志并保存可用帧。现有镜牢6次调用失败后抛错，不加载编队码/确认；日常既有False阻止战斗。

## 验证证据
- `research/red.txt`：原实现17 failed、3 passed，涵盖危险左键拖动与视觉错选/无界截图。
- `research/red-ocr.txt`：OCR异常逃逸1 failed、27 passed；现已转成失败结果。
- `research/red-prompt.txt`：验证保留原首页提示关闭行为；修复后全绿。
- `research/regression.txt`：`.venv/Scripts/python.exe -m pytest tests -q` → **303 passed in 10.17s**。
- `research/lint.txt`：`.venv/Scripts/python.exe -m ruff check module/automation/input_handlers/input.py tasks/team_list.py tasks/teams/team_formation.py tests --ignore E722` → All checks passed。
- compileall（3产品文件+3新增测试文件）和 `git diff --check` 退出0。未配置独立类型检查器，未安装依赖。
- `research/offline-crop-ocr.txt`：读取用户既有裁剪截图，使用现有 RapidOCR/ONNX 模型，无下载、无游戏输入，解析到剧情关卡、编队#3、编队#4及其后续。由于裁剪图不含橡皮擦，离线验证仅以已知列表标题构造参考坐标来验证解析，不是完整页面定位验证。

## 边界检查
- 半行、1行、3行、5行位移均由画面决定，测试覆盖1/3/8/35/40项、连续40→2→35→1、列表初始处于中段、错误点击纠正。
- OCR空/异常、截图连续失败/暂时失败、滚动无进展、目标缺失、同页/远端重名、预设与#20前缀、列表文本不能冒充选中标题。
- 前台/后台坐标与光标恢复、发送异常、无句柄、暂停门闩、Automation交互门、window_move拒绝与模拟器专用接口分支。
- 镜牢失败不确认/加载编队码；日常两种入口失败传播回归在全套内通过。

## 明确限制 / 主会话待核对
- 未运行真实游戏输入，未复现历史重排。1600×900后台滚轮实际响应、完整画面OCR标题位置、模拟器真实位移及连续无人值守仍未验证。
- 为避免未证实的归顶与跨页重名，每次选队扫描全部40槽；比旧方案多出OCR/滚动开销。非40槽布局保守失败。重名或OCR模糊不猜测放行。
- 纯解析的列表可视范围与标题区域由既有1440基准布局及用户截图约束；非标准UI布局会失败，不能声称已兼容所有布局。
- 主会话需审查diff、独立重跑验证，并按计划更新spec（推荐记录：序号≠名称编号；Windows禁止条目拖动；滚轮刻度不是像素；失败传播必须禁止确认）。子代理未改spec/task状态，未提交、推送、合并或覆盖发行目录。

## 文件
修改：`module/automation/input_handlers/input.py`、`tasks/teams/team_formation.py`、`CHANGES.md`。
新增：`tasks/team_list.py`、`tests/test_team_visual_selection.py`、`tests/test_team_list_parser.py`。
接续完善已有未跟踪文件：`tests/test_team_safe_input.py`。
任务证据：当前任务 `research/`。其他未跟踪任务目录未动。
