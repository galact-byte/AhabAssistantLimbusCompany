# 设计：镜牢商店误判与离开恢复

## 1. 目标与边界

本设计切断「地图金币 HUD → 误进商店 → 退不出 → 重启」循环，并让后台点击下的 farthest 缩放后备真正执行。不重写商店内治疗/买卖/合成，不改模板匹配底层，不把金币坐标当商店/地图的区分条件。

共享识别必须是无副作用纯函数：输入 OCR 文本与模板命中分数，输出 `shop` / `map` / `unknown`。主循环、寻路里的商店拦截、离开循环都消费同一结果。

## 2. 状态与出口

| 状态 | 识别条件 | 动作 | 成功后状态 | 超时或失败出口 |
| --- | --- | --- | --- | --- |
| 镜牢地图 | OCR「正在探索第N层」，或 `legend_assets` ≥ 地图阈值（日志 0.777，默认 0.8 会漏） | 不进商店；离开循环视为已离开 | 主循环寻路 | 不得 `back_init_menu` |
| 地图但 `shop_coins` ≥0.96 | 同上，即使金币模板命中 | 视为地图 | 主循环寻路 | 不得进 `in_shop()` |
| 真商店 | `shop_coins` 命中，且至少一项专属控件（离开 / 治疗 / 商店返回），且无地图证据 | 进入 `in_shop()` | 商店流程结束后离开循环 | 证据不足则 `unknown`，不进商店 |
| 离开商店 | 已完成商店动作 | 点离开/确认；每轮复用地图识别 | 地图 | 地图证据出现即结束；耗尽才走原 `back_init_menu` |
| 后台 farthest | nearest 三次失败且 `background_click` | 调用 farthest；后台滚轮发 `WM_MOUSEWHEEL` | 进门或下一节点 | 滚轮/缩放失败返回 `False`，继续进门后备；不抛未处理 `InputAttributeError`，不立刻重进镜牢 |

## 3. 共享识别契约

新增轻量模块 `tasks/mirror/shop_presence.py`，不得导入 `Automation`、OCR 引擎、`cfg`、日志、睡眠或点击。不要放进 `tasks/mirror/__init__.py`（该文件会扫资源目录）。

```python
from dataclasses import dataclass
from typing import Literal

MAP_LEGEND_THRESHOLD = 0.75
SHOP_CONTROL_THRESHOLD = 0.8

@dataclass(frozen=True)
class ShopPresence:
    state: Literal["shop", "map", "unknown"]
    reason: str


def resolve_mirror_shop_presence(
    ocr_texts: list[str],
    *,
    shop_coins: float | None = None,
    legend: float | None = None,
    leave: float | None = None,
    heal: float | None = None,
    shop_return: float | None = None,
) -> ShopPresence:
    ...
```

判定顺序：

1. **地图否决**：任一 OCR 文本匹配 `正在探索第`+层，或 `legend >= MAP_LEGEND_THRESHOLD` → `map`。`shop_coins` 再高也否决。
2. **商店确认**：`shop_coins` 达到现有默认图像阈值，且 `leave` / `heal` / `shop_return` 至少一项达到 `SHOP_CONTROL_THRESHOLD` → `shop`。
3. **否则** `unknown`：主循环不进商店；离开循环不把它当已离开。

调用方负责截图和 `find_element`；纯函数只看分数与文本。三处 `shop_coins`（`mirror.py` 约 136 / 287 / 407）必须走同一辅助函数，禁止复制布尔表达式。

## 4. 运行时编排

### 4.1 进入商店

主循环现有 `if auto.find_element("mirror/shop/shop_coins_assets.png")` 改为调用共享辅助函数。该辅助函数：

- 读取当前帧 OCR（优先 `get_ocr_entries()` / 已有全图 OCR 缓存，避免热路径重复识别）；
- 采集 `shop_coins`、`legend`、离开、治疗、商店返回的相似度（调用方或薄封装拿到分数；不要只拿 True/False，否则 0.777 的 legend 会被默认 0.8 丢掉）；
- `state == "shop"` 才 `in_shop()`；`map` / `unknown` 都跳过。

寻路分支里「看到 shop_coins 就 continue」同样改用该结果：只有真商店才让出给商店流程；地图金币 HUD 必须继续寻路。

拿相似度而不是布尔命中：现有 `find_element` 默认 0.8 会吞掉 0.777 的 legend。允许新增「返回 (center, score)」的薄查询，或对 legend 使用 `threshold=MAP_LEGEND_THRESHOLD` 并把分数传入解析器。禁止把默认 0.8 写死进商店识别。

### 4.2 离开商店

`in_shop()` 离开循环第一优先改为共享解析：`map` → `break`，不点离开、不打「无法退出商店」。真商店才点 `leave_assets` / `leave_shop_confirm`。循环耗尽且仍非地图时，保留原 `back_init_menu()`。

### 4.3 后台 farthest

`BackgroundInput.mouse_scroll` 不再固定 `False`。沿用现有 `PostMessage`/`SendMessage` 点击路径发送 `WM_MOUSEWHEEL`（滚轮增量与前台 `pyautogui.scroll(-3)` 同语义：缩小地图）。成功发送返回 `True`。不实现模拟器滚轮，不改 `WindowMoveInput`。

`search_road_farthest_distance()`：`mouse_scroll()` 为 `False` 时返回 `False`，不再抛 `InputAttributeError`。

`Mirror.search_road()`：删除 `if cfg.background_click: continue`。后台与前台一样跑 farthest 三次。滚轮发出但 Unity 忽略时，`mybus_maximum_distance` 找不到 → farthest 返回 `False` → 既有 `enter_assets` 后备。只有全部后备失败才进入原「寻路出错, 尝试重进镜牢」。

## 5. 失败模型与日志

| 结果 | 日志级别 | 文案要点 |
| --- | --- | --- |
| 地图否决商店 | `debug` | 原因 `map_ocr` / `map_legend`，不打 OCR 全文 |
| 证据不足跳过商店 | `debug` | `unknown` |
| 确认真商店 | 保持现有「开始执行 镜牢商店」 | 不新增噪音 |
| 离开循环因地图结束 | `debug` | 已在地图，结束离开 |
| 离开耗尽仍非地图 | 保持现有 `error`「无法退出商店」 | 仅真卡死 |
| 后台滚轮已发送 | `debug` | 不刷每帧 |
| farthest 因滚轮不可用失败 | `debug` 或 `warning` | 降级，不是 `error` 重开 |

禁止记录截图像素、完整 OCR 列表、账户或配置倾倒。

## 6. 兼容与回滚

- 前台滚轮、键盘寻路、onnx 路线图行为不变。
- 真商店仍进入；忽略楼层商店的现有开关不变。
- Unity 忽略后台 `WM_MOUSEWHEEL` 时，最坏是 farthest 无效，行为回到「nearest + 进门」，不再因空跳/异常提前重开。
- 回滚：还原 `shop_presence.py`、三处商店判定、离开循环、`BackgroundInput.mouse_scroll`、farthest 与 `search_road` 跳过逻辑。

## 7. 风险

- 商店专属模板在部分楼层/语言下偏低：R1 选择「漏进商店优于误进」。若实机真商店被跳过，再加控件，不降低地图否决。
- `get_ocr_entries()` 热路径成本：复用 `_run_full_ocr` 缓存。
- 后台 `WM_MOUSEWHEEL` 对 Unity 可能无效：契约是降级，验收不把「后台缩放一定成功」写成硬条件。
