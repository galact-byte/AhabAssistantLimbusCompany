# 镜牢商店误判与离开恢复

## Goal

夜间无人值守刷镜牢时，不得把地图金币 HUD 当成商店并反复重启；一旦误入商店流程，必须识别“其实还在地图”并回到寻路。后台点击模式下 nearest 寻路失败后，仍须尝试 farthest 缩放后备，不得因滚轮不支持而直接重进镜牢。

## Background

证据来自 `G:\BaiduNetdiskDownload\AALC_v1.5.3\AALC\logs\debugLog.log`（2026-09-05 挂机）。同一帧同时出现：

| 信号 | 实测 | 真实界面 |
| --- | --- | --- |
| OCR | `正在探索第1层` / `身无分文的赌徒` | 镜牢地图 |
| `mirror/road_in_mir/legend_assets.png` | 0.777 @ (1557, 127) | 地图图例 |
| `mirror/shop/shop_coins_assets.png` | **0.96 @ (1360, 57)** | 右上角金币 HUD |

`tasks/mirror/mirror.py` 约 407 行只要 `shop_coins_assets` 命中就调用 `in_shop()`，不再确认离开/治疗等商店专属控件。地图金币与商店金币都在右上角，坐标不能当区分条件。随后：

1. 治疗模板对不上（约 0.25 / 0.36），商店金币框 OCR 读到地图文字，报「获取剩余金钱失败」。
2. 离开循环点不到 `leave_assets`（0.11–0.38）。
3. 退出条件是 `legend_assets` 默认阈值 0.8，地图实测 0.777，即使已在地图也退不出。
4. 30 次后「无法退出商店」→ `back_init_menu()` → 关游戏重启。

03:10–04:17 该循环至少 6–8 轮。叠加：`background_click: true` 时 `search_road()` 故意跳过 `search_road_farthest_distance()`（`mirror.py` 约 1082 行），因为该函数依赖 `mouse_scroll()`，`BackgroundInput.mouse_scroll()` 固定返回 `False`，函数会抛 `InputAttributeError`。重启后寻路再失败，把商店误判放大成「误判 ↔ 寻路失败」循环。

同日志后半段纽本失败取消剩余任务、以及 04:17–12:49 的 8.5 小时空白，不是本任务范围。

## Requirements

### R1 商店进入必须有完整商店证据

镜牢主循环不得仅凭 `mirror/shop/shop_coins_assets.png` 进入商店。必须同时满足：

- 没有地图证据：OCR「正在探索第N层」或足够可信的 `legend_assets`（日志实测 0.777，默认 0.8 会漏）；
- 且至少一项商店专属控件（离开、治疗入口或商店返回）。

证据不足时不得进入商店。漏一次真商店可接受；误进商店后重启不可接受。

涉及：`tasks/mirror/mirror.py` 约 136、287、407 行，三处 `shop_coins` 判定共用同一识别契约。

### R2 离开商店：已在地图即视为已离开

`in_shop()` 离开循环遇到地图证据时必须结束并交回主循环寻路，不得继续点 `leave_assets`，不得打「无法退出商店」，不得 `back_init_menu()` 重启。

涉及：`tasks/mirror/in_shop.py` 约 1414–1439 行。

### R3 回归测试

为 R1 / R2 / R4 建立不依赖实机的 pytest。先红后绿。至少覆盖：

- 日志同款信号（`shop_coins` 0.96 + 地图 OCR/图例 0.777）不得进商店；
- `shop_coins` + 商店专属控件、无地图证据时应进商店；
- 离开循环遇到 `legend` 0.777 / 「正在探索」应结束而不是重启；
- 后台点击下 farthest 不再被空跳；滚轮仍失败时不得立刻「寻路出错, 尝试重进镜牢」。

### R4 后台点击下 farthest 寻路必须可执行或可降级

`background_click: true` 时不得空跳 `search_road_farthest_distance()`。后台输入须能发出与前台滚轮同语义的缩放（失败返回 `False`，不抛未处理异常）。若滚轮仍不被游戏接受，`search_road()` 须把 farthest 标为不可用并继续既有 nearest / 键盘 / 进门后备，不得立刻重进镜牢。

不实现模拟器滚轮，不重写 onnx 路线图。

涉及：`module/automation/input_handlers/input.py` 的 `BackgroundInput.mouse_scroll`、`tasks/mirror/search_road.py` 约 238–242 行、`tasks/mirror/mirror.py` 约 1082–1100 行。

## Non-Goals

- 不修纽本失败取消后续任务（已有 `08-08-daily-event-state-machine`）。
- 不修 04:17–12:49 的 Steam 等待 / 电脑休眠挂起。
- 不重写商店内治疗、买卖、合成、刷新逻辑。
- 不改 OCR / 模板匹配底层，不为该问题换新依赖。
- 不实现模拟器滚轮，不把后台滚轮推广成通用输入重构。
- 不把金币坐标当作商店/地图的区分条件。

## Acceptance Criteria

- [ ] 地图帧（`shop_coins` 高相似 + OCR「正在探索第N层」和/或 `legend_assets` ≈0.777）不得进入商店流程。
- [ ] 真商店帧（`shop_coins` + 至少一项商店专属证据，且无地图证据）仍进入商店。
- [ ] 三处 `shop_coins` 调用点共用同一识别结果，不出现一处修、两处仍误判。
- [ ] 离开循环遇到地图证据时结束并回到主循环，不打「无法退出商店」、不 `back_init_menu`。
- [ ] `background_click: true` 时 `search_road()` 会调用 farthest；后台 `mouse_scroll` 不再固定 `False`。
- [ ] 滚轮仍失败时 farthest 返回失败并走既有后备，不因 `InputAttributeError` 立刻重进镜牢。
- [ ] 新增 pytest 覆盖上述条款；先红后绿。
- [ ] 全量 `uv run pytest` 通过；Ruff 范围检查不新增违规。
- [ ] 实机：镜牢过商店节点不再因地图 HUD 误判而重启；后台点击下 nearest 失败后不再因跳过 farthest 立刻重开（用户执行；该项通过前不宣称已修复）。

## Key Decisions

- 商店误判与后台 farthest 同一次交付。farthest 被跳过会把商店误判放大成重启循环，拆到下次会让夜间挂机继续卡死。
- 证据不足时跳过商店，不重启。无人值守下漏一次治疗/购物优于关游戏。
- 后台滚轮按现有 `PostMessage`/`SendMessage` 点击路径补 `WM_MOUSEWHEEL`；Unity 若仍忽略滚轮，契约是降级而不是重启。
