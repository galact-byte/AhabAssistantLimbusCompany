# 镜牢商店误判与离开恢复：实施计划

**Goal:** 用地图否决 + 商店专属控件阻止金币 HUD 误进商店；离开循环在已回到地图时结束；后台点击下 farthest 真正调用，滚轮失败则降级而不是重开。

**Architecture:** `tasks/mirror/shop_presence.py` 持有无副作用识别契约；`mirror.py` 三处商店判定与 `in_shop()` 离开循环共用该结果。`BackgroundInput.mouse_scroll` 发 `WM_MOUSEWHEEL`；`search_road_farthest_distance()` 失败返回 `False` 而不抛。

**Tech Stack:** Python 3.12、pytest、Ruff、现有 RapidOCR 缓存与 OpenCV 模板分数。不新增依赖。

## 全局约束

- 不新增第三方依赖；保持现有中文路径。
- 纯识别函数不得截图、睡眠、点击、读 `cfg`、写日志或改全局状态。
- 不要把模块放进 `tasks/mirror/__init__.py`（会扫资源目录）。
- 三处 `shop_coins` 必须走同一辅助函数，禁止复制布尔表达式。
- 不得用金币坐标区分商店/地图。
- 证据不足时跳过商店，不重启。
- 不实现模拟器滚轮，不改 `WindowMoveInput`。
- 不重置既有商店内治疗/买卖/合成逻辑。
- 执行前载入 `.trellis/spec/backend/{index,error-handling,logging-guidelines,quality-guidelines}.md` 与 `.trellis/spec/guides/code-reuse-thinking-guide.md`。

---

## 文件职责地图

| 文件 | 改动职责 |
| --- | --- |
| `tasks/mirror/shop_presence.py` | 新建。`ShopPresence`、`MAP_LEGEND_THRESHOLD`、`resolve_mirror_shop_presence()`。 |
| `tasks/mirror/mirror.py` | 三处 `shop_coins` 改为共享识别；删除后台 farthest 空跳。 |
| `tasks/mirror/in_shop.py` | 离开循环优先消费地图识别；`map` 则结束。 |
| `tasks/mirror/search_road.py` | `mouse_scroll()` 失败返回 `False`，不再抛 `InputAttributeError`。 |
| `module/automation/input_handlers/input.py` | `BackgroundInput.mouse_scroll` 发 `WM_MOUSEWHEEL`，成功返回 `True`。 |
| `tests/test_mirror_shop_presence.py` | 纯解析 + 进入/离开编排 + 后台 farthest 降级。 |
| `CHANGES.md` | 全部自动化和实机验收完成后记录行为变更。 |

## 公共接口契约

Task 1 产出以下接口；后续任务只能依赖这些名称和含义：

```python
# tasks/mirror/shop_presence.py
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
    """仅从 OCR 文本和模板分数判定地图、商店或证据不足。"""
```

- `map`：OCR 含「正在探索第N层」，或 `legend >= MAP_LEGEND_THRESHOLD`。`reason` 为 `map_ocr` / `map_legend`。
- `shop`：`shop_coins` 达默认图像阈值，且离开/治疗/商店返回至少一项达 `SHOP_CONTROL_THRESHOLD`，且不是 `map`。
- `unknown`：其余情况。调用方不进商店，离开循环不把它当已离开。

运行时薄封装（可与纯函数同文件或放在 `mirror.py` 私有辅助）负责截图、取分数、读 OCR 缓存；测试纯解析时不得实例化 `Automation`。

---

## Task 1：纯识别契约（Red → Green）

**Files:**
- Create: `tasks/mirror/shop_presence.py`
- Create: `tests/test_mirror_shop_presence.py`

**Produces:** `ShopPresence`、`resolve_mirror_shop_presence()`；Task 2–4 使用。

- [ ] **Step 1：写会失败的解析测试。**

  至少断言：

  1. 日志同款：OCR `正在探索第1层` + `shop_coins=0.96` + `legend=0.777` → `map`，`reason=map_ocr` 或 `map_legend`。
  2. 仅 `legend=0.777`、无 OCR → `map`。
  3. `legend=0.74` 且无探索 OCR、无商店控件 → `unknown`。
  4. `shop_coins=0.96` + `leave=0.85`、无地图证据 → `shop`。
  5. 仅 `shop_coins=0.96`、无控件、无地图 → `unknown`。
  6. 商店控件与探索 OCR 同时存在 → 仍 `map`（地图否决优先）。

- [ ] **Step 2：运行 `uv run pytest tests/test_mirror_shop_presence.py`，确认红灯。**
- [ ] **Step 3：实现纯函数，再跑同一文件至绿灯。**
- [ ] **Step 4：`uv run ruff check tasks/mirror/shop_presence.py tests/test_mirror_shop_presence.py --ignore E722`。**

---

## Task 2：主循环与离开循环接入（Red → Green）

**Files:**
- Modify: `tasks/mirror/mirror.py`（约 136、287、407）
- Modify: `tasks/mirror/in_shop.py`（约 1414–1439）
- Modify: `tests/test_mirror_shop_presence.py`

**Consumes:** Task 1 契约。

- [ ] **Step 1：写编排测试（mock `auto`，不接游戏）。**

  1. 地图帧不得调用 `in_shop()`。
  2. 真商店帧调用 `in_shop()`。
  3. 寻路分支里地图金币 HUD 不得 `continue` 让出给商店。
  4. 离开循环在 `map` 时结束，不打「无法退出商店」，不调用 `back_init_menu`。
  5. 三处判定若无法直接测私有循环，至少测共享运行时辅助函数对上述帧的返回值，并静态确认三处都调用它。

- [ ] **Step 2：确认新测试红灯。**
- [ ] **Step 3：接入辅助函数；离开循环第一优先 `map` → `break`。**
- [ ] **Step 4：相关 pytest + ruff 通过。**

拿相似度时：legend 使用 `MAP_LEGEND_THRESHOLD`（0.75），不要默认 0.8。优先复用 `_run_full_ocr` / `get_ocr_entries()` 缓存。

---

## Task 3：后台 farthest（Red → Green）

**Files:**
- Modify: `module/automation/input_handlers/input.py`（`BackgroundInput.mouse_scroll`）
- Modify: `tasks/mirror/search_road.py`（约 238–242）
- Modify: `tasks/mirror/mirror.py`（约 1082–1100）
- Modify: `tests/test_mirror_shop_presence.py` 或新建 `tests/test_mirror_background_farthest.py`

- [ ] **Step 1：写失败测试。**

  1. `BackgroundInput.mouse_scroll` 在可注入的 Post/Send 下发出 `WM_MOUSEWHEEL` 并返回 `True`（mock hwnd / win32，不碰真窗口）。
  2. `search_road_farthest_distance()` 在 `mouse_scroll()` 为 `False` 时返回 `False`，不抛 `InputAttributeError`。
  3. `search_road()` 在 `background_click=True` 时仍调用 farthest；farthest `False` 后走 `enter_assets` 后备，不立刻打「寻路出错, 尝试重进镜牢」。

- [ ] **Step 2：确认红灯。**
- [ ] **Step 3：实现滚轮消息；删除空跳；farthest 失败返回 `False`。**
- [ ] **Step 4：相关 pytest + ruff 通过。**

滚轮增量与前台 `pyautogui.scroll(-3)` 同语义（缩小）。沿用该类现有 `use_post_message` 分支。不实现模拟器滚轮。

---

## Task 4：全量验证

- [ ] `uv run pytest`
- [ ] `uv run ruff check tasks/mirror/shop_presence.py tasks/mirror/mirror.py tasks/mirror/in_shop.py tasks/mirror/search_road.py module/automation/input_handlers/input.py tests/test_mirror_shop_presence.py --ignore E722`
- [ ] 确认未改商店治疗/买卖/合成主逻辑，未改 `tasks/mirror/__init__.py`。
- [ ] 实机项保持未勾：用户夜间挂机过商店节点、后台 nearest 失败后的 farthest 行为。通过前不宣称已修复。

## 回滚点

1. Task 1 仅新增文件，可删。
2. Task 2 改判定与离开循环；回滚这两处即恢复误判行为。
3. Task 3 改输入与寻路；回滚后后台仍跳过 farthest。

## 风险

- 真商店模板分数偏低会被 `unknown` 跳过：按 PRD，漏一次优于误进。实机若漏，只加控件，不降低地图否决。
- Unity 忽略 `WM_MOUSEWHEEL`：farthest 无效，但不再提前重开。

## 归档判定（2026-09-25）

商店判定、地图离店和后台滚轮的实现及 `tests/test_mirror_shop_presence.py` 等回归已在当前仓库；本次整库检查为 314 passed。用户表示已在实机测试，觉得没有明显问题，并明确要求归档。本任务按用户体验验收关闭；实施清单是原设计步骤，未逐项留下 RED 输出或夜间 nearest 失败后 farthest 的实机日志，不能把未勾项追记为已独立验证。如后续出现同类挂机问题，以新的日志另立问题继续排查。
