# Error Handling

> Executable error-handling conventions for the Python automation layer.

## Overview

Automation loops must expose a bounded, explicit outcome instead of treating an unrecognized frame as the next navigation screen. For the daily battle flow, callers use `None` for “not this state”, `True` for “handled; retry the current loop”, and `False` for “terminal failure; do not continue this action”.

## Scenario: Daily event page and entry recovery

### 1. Scope / Trigger

- Trigger: a beta event result page can remain visible after battle while its template button is unavailable for about 40 seconds.
- Scope: `Battle.fight()`, `back_init_menu()`, and daily EXP/Thread entry navigation.
- Goal: an event result page must not be treated as a failed Thread entry, and recovery must have an explicit upper bound.

### 2. Signatures

```python
# tasks/event_page.py
OcrBounds = tuple[int, int, int, int]
OcrEntry = tuple[str, OcrBounds]

@dataclass(frozen=True)
class EventPageResolution:
    state: Literal["advance", "wait"]
    position: tuple[int, int] | None
    reason: str


def resolve_event_page(entries: list[OcrEntry]) -> EventPageResolution | None: ...

# tasks/daily/luxcavation.py
MAX_ENTRY_RECOVERY_ATTEMPTS = 1

def _recover_daily_entry(recovery_attempts: int, log_prefix: str) -> bool: ...
```

### 3. Contracts

| Input / outcome | Contract |
| --- | --- |
| `advance` | The OCR parser found an event action and supplies the target text-box center in `position`. |
| `wait` | A result (`判定成功` / `判定失败`) is visible but its continuation is not; `position` is `None`. |
| `None` | The OCR frame does not prove an event page; preserve the caller’s pre-existing state handling. |
| `advance` with `position is None` | Treat as bounded `wait`; never unpack or click `None`. |
| `back_init_menu(allow_restart=False)` event timeout | Return `False`; do not press ESC, click blank space, kill, or restart. |
| Daily entry budget exhausted | Run `_recover_daily_entry()` at most once; recovery failure or a second exhaustion returns `False`. |

`Battle.fight()` may reset its local `chance` for `advance` or `wait`, but must not reset `start_time`; the existing total battle timeout remains authoritative. `back_init_menu()` waits at most `EVENT_PAGE_WAIT_TIMEOUT` seconds according to `monotonic()` and refreshes its ordinary loop budget while that event-specific clock is active.

### 4. Validation & Error Matrix

| Condition | Required behavior |
| --- | --- |
| Result + `继续` OCR | Click the OCR center, log debug, continue the current loop. |
| Result without action | Wait one second, retain only the bounded event timer, continue. |
| OCR action template works | Keep the template-first path; do not run the OCR fallback first. |
| Server-error handler returns `True` | Skip normal page/event recognition for that iteration. |
| Server-error handler returns `False` | Stop the current action; do not continue navigation. |
| Event wait exceeds 60 seconds | `allow_restart=False`: return `False`; otherwise reuse the established restart branch. |
| Entry recovery succeeds once | Reset entry loop state and perform one complete retry. |
| Entry recovery is unavailable or already used | Return `False`; callers must not select a team or start battle. |
| Choice page first button is grey | Do not invoke the first-choice template; click only the OCR-located second slot. |
| Choice page first button is not grey | Retry only the first slot (template first, OCR fallback); never infer grey state merely because the page persisted. |
| Choice page has no OCR candidate or does not advance repeatedly | After `EVENT_CHOICE_MAX_RETRY_ATTEMPTS`, return `False`; do not wait for the total battle timeout. |
| Daily battle exits without `战斗胜利 + 确认` settlement | Return `False`; callers must cancel the daily group and top-level task sequence. |

### 5. Good / Base / Bad Cases

- **Good:** `判定成功` and `继续` are both OCR-visible; click the continuation center and resume battle.
- **Base:** a result remains visible during its animation; wait without consuming the battle chance or the general return-home loop budget.
- **Bad:** a standalone `继续` or `进行判定` is insufficient evidence. A “进行判定” target must have a separate event-context OCR entry; the button text itself cannot supply that context.

### 6. Tests Required

- Pure parser tests must import `tasks.event_page` and run without RapidOCR installed.
- Test result success and failure without a button → `wait`; result plus continuation → `advance` at the OCR center.
- Test all event contexts (`事件`, `判定`, `选项`) and ensure standalone/annotated “进行判定” buttons do not self-authorize.
- Test `Battle.fight()` with an exhausted local chance: wait and advance must still reach settlement; removing either reset must fail the test.
- Test `back_init_menu()` after 40 event-wait iterations, at 60-second timeout, after a non-event reset, and with `allow_restart=False`.
- Parameterize EXP and Thread entry tests for one recovery success, recovery failure, renewal-recovery failure, and second exhaustion.
- Test grey first choice → second-slot click, enabled first choice → first-slot retry, absent candidate → bounded `False`, and repeated non-advancing candidate → bounded `False`.
- Test a battle exit without daily settlement and each propagation boundary: single daily process, group, wrapper, startup-resume path, and top-level task sequence.

### 7. Wrong vs Correct

#### Wrong

```python
if loop_count < 0:
    return False
# A result animation can exhaust this 30-iteration budget before its button appears.
```

#### Correct

```python
if event_wait_started_at is not None and monotonic() - event_wait_started_at < EVENT_PAGE_WAIT_TIMEOUT:
    loop_count = LOOP_COUNT
    sleep(1)
    continue
```

The monotonic event timer, not the general navigation loop, controls event-result patience.

## Scenario: Windows Steam launch and graceful exit recovery

### 1. Scope / Trigger

- Trigger: a forced game termination can leave Steam cloud synchronization incomplete; the next Steam launch can show the Chinese “无法同步” confirmation while the Unity process exists but the game window is not ready.
- Scope: `module.game_and_screen.game`, `module.game_and_screen.steam_cloud`, `module.game_and_screen.screen`, `tasks.base.script_task_scheme`, and every Windows restart/exit caller.
- Goal: perform one bounded launch request, automatically confirm only the user-authorized cloud-sync dialog, and avoid unnecessary forced process termination.

### 2. Signatures

```python
# module/game_and_screen/steam_cloud.py
@dataclass(frozen=True)
class SteamCloudDialog:
    continue_position: tuple[int, int]
    continue_bounds: OcrBounds


def resolve_steam_cloud_dialog(entries: list[OcrEntry]) -> SteamCloudDialog | None: ...
def handle_steam_cloud_sync_dialog(*, on_dialog_detected: Callable[[], None]) -> bool: ...

# module/game_and_screen/game.py
def start_game(self) -> bool: ...
def handle_pending_launch(self) -> bool: ...
def finish_launch_attempt(self) -> None: ...
def close_game(self) -> bool: ...

# module/game_and_screen/screen.py
def init_handle(self, start_if_missing: bool = True) -> bool: ...
```

### 3. Contracts

| Input / outcome | Contract |
| --- | --- |
| Existing game process, no window | Create a pending launch state; do not re-open Steam, but permit one cloud-dialog scan during the bounded wait. |
| Pending launch | `start_game()` is idempotent while the request is pending; no second local-path or Steam URL launch. |
| Valid cloud dialog | Require normalized Chinese title `无法同步`, body fragments `未能将您的存档` and `Steam 云同步`, an exact `仍然进行游戏` button, button below the body, and all anchors in one bounded desktop region. |
| Valid cloud dialog click | Call `on_dialog_detected` before desktop click so a thrown click cannot authorize a second attempt in the same pending launch. |
| Missing/ambiguous dialog evidence | Do not click any Steam control; retain the bounded launch wait only. |
| Launch timeout | Clear pending state and raise `withOutGameWinError`; callers must stop the current task instead of retrying Steam indefinitely. |
| Windows exit | Clear pending state, send `WM_CLOSE` to a valid game window, wait `GAME_GRACEFUL_CLOSE_TIMEOUT_SECONDS`, then use the sole `taskkill /F /IM <exact process name>` fallback. |

### 4. Validation & Error Matrix

| Condition | Required behavior |
| --- | --- |
| Configured local game path exists | Use `os.startfile` once and log the local launch. |
| Configured path missing | Log once with the path-repair hint, then request Steam URL once. |
| Full process filename has different case | Treat it as the game process. |
| Process name merely contains the configured name | Treat it as unrelated; do not suppress launch or terminate it. |
| Cloud anchors come from different desktop regions | Return `None`; never click. |
| Click throws after target recognition | Consume the single confirmation attempt and return `False`; do not retry clicking. |
| Normal close completes during grace period | Do not run `taskkill`. |
| Normal close times out | Log a warning and use the single centralized process-name fallback. |

### 5. Good / Base / Bad Cases

- **Good:** `init_game()` launches once, polls `screen.init_handle(start_if_missing=False)`, sees the complete cloud dialog, consumes its one authorization, clicks `仍然进行游戏`, then receives the game window.
- **Base:** the Unity process exists while Steam still owns the confirmation; keep a pending state and wait up to the launch deadline without re-opening Steam.
- **Bad:** each missing-window poll calls `webbrowser.open`, or a generic desktop OCR keyword clicks a button in another Steam window.

### 6. Tests Required

- Pure dialog tests must reject missing anchors, cancel-only dialogs, a button above the body, and anchors split across desktop regions.
- Test one Steam URL request per pending launch, existing-process pending behavior, local-path preference, and launch-timeout cleanup.
- Test a click exception consumes the confirmation attempt.
- Test exact case-insensitive process matching and reject a similarly named process.
- Test `WM_CLOSE` first, no force kill on normal exit, force kill only on timeout, and every Windows exit/restart wrapper delegates to `Game.close_game()`.
- Top-level script tests that do not test image recognition must stub `auto.click_element`; they must never access the real screenshot/window/process stack.

### 7. Wrong vs Correct

#### Wrong

```python
while not screen.init_handle():
    game_process.start_game()  # Re-opens Steam while a cloud dialog blocks startup.
```

#### Correct

```python
if game_process.start_game():
    while monotonic() < deadline:
        if screen.init_handle(start_if_missing=False):
            game_process.finish_launch_attempt()
            break
        game_process.handle_pending_launch()
        sleep(1)
```

## Scenario: Mirror shop false-positive and farthest fallback

### 1. Scope / Trigger

- Trigger: the map gold HUD matches `mirror/shop/shop_coins_assets.png` at ≥0.96 while OCR still reads `正在探索第N层` and `legend_assets` scores about 0.777.
- Scope: `tasks.mirror.shop_presence`, `Mirror` shop entry, `Shop.in_shop()` leave loop, `search_road_farthest_distance()`, `BackgroundInput.mouse_scroll`.
- Goal: never enter shop from coins alone; if already on the map, leave without `back_init_menu()`; background farthest must run or degrade, never restart because scroll is missing.

### 2. Signatures

```python
# tasks/mirror/shop_presence.py
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
) -> ShopPresence: ...

def inspect_mirror_shop_presence(auto) -> ShopPresence: ...
def should_end_shop_leave(presence: ShopPresence) -> bool: ...
def is_on_mirror_map(auto, *, use_ocr: bool = True) -> bool: ...
```

### 3. Contracts

| Input / outcome | Contract |
| --- | --- |
| `map` | OCR matches `正在探索第.+层`, or `legend >= 0.75`. Coins at 0.96 cannot override this. |
| `shop` | Coins meet the default image threshold **and** leave / heal / shop-return meets 0.8, **and** the frame is not `map`. |
| `unknown` | Skip shop. Do not restart. Leave loop does not treat this as already left. |
| Leave loop sees `map` | `break`; no `无法退出商店`; no `back_init_menu()`. |
| `mouse_scroll()` is `False` | `search_road_farthest_distance()` returns `False`; do not raise `InputAttributeError`. |
| `background_click` | Still call farthest. If it fails, keep the existing enter-door fallback. |
| Map gate (`is_on_mirror_map`) | `legend >= 0.75`, then optional OCR. Battle / `back_init_menu` pass `use_ocr=False`. |

Callers must feed raw similarity scores. `find_element(..., threshold=0.8)` drops a 0.777 legend and must not be the shop/map gate. Pathfinding, reward-card, theme-pack, battle, and return-home map gates must use `is_on_mirror_map`, not default `find_element`.

### 4. Validation & Error Matrix

| Condition | Required behavior |
| --- | --- |
| Logged map HUD (`shop_coins=0.96`, OCR `正在探索第1层`, legend 0.777) | `map`; do not call `in_shop()`. |
| Coins + leave, no map evidence | `shop`; enter `in_shop()`. |
| Coins only | `unknown`; skip shop. |
| Leave loop on map evidence | End; resume pathfinding. |
| Background scroll unavailable | farthest `False`; do not log `寻路出错, 尝试重进镜牢` yet. |

### 5. Good / Base / Bad Cases

- **Good:** map OCR vetoes coins and shop controls; pathfinding continues.
- **Base:** true shop has coins plus leave/heal/return and no map OCR/legend.
- **Bad:** coins alone, or coins plus a default-0.8 legend miss, must not enter shop or restart.

### 6. Tests Required

- Pure `resolve_mirror_shop_presence()` tests import `tasks.mirror.shop_presence` without instantiating `Automation`.
- Logged HUD, legend-only, coins-only, coins+leave, and map-veto-over-controls cases.
- Runtime inspect helper and all three `shop_coins` sites share it.
- Leave loop ends on `map` without `back_init_menu`.
- `is_on_mirror_map()` accepts logged legend 0.777; battle and `back_init_menu` call it with `use_ocr=False`.
- farthest returns `False` when scroll is `False`; `search_road()` does not skip farthest under `background_click`.
- `BackgroundInput.mouse_scroll` emits `WM_MOUSEWHEEL` (mocked hwnd; no live window).

### 7. Wrong vs Correct

#### Wrong

```python
if auto.find_element("mirror/shop/shop_coins_assets.png"):
    self.in_shop()
if not auto.mouse_scroll():
    raise InputAttributeError("后台输入不支持滚轮操作!")
```

#### Correct

```python
if inspect_mirror_shop_presence(auto).state == "shop":
    self.in_shop()
if not auto.mouse_scroll():
    return False
```

## Scenario: Mirror pathfinding ONNX-None and on-map recovery

### 1. Scope / Trigger

- Trigger: `identify_nodes()` (ONNX) returns `None` on the mirror map, or `mybus_default_distance.png` is never located, so `search_road_from_road_map()` used to feed `None` / a `None` bus into `divide_the_area_by_*` / `bus[0]` and raise `TypeError` (issue #893).
- Trigger: `search_road()` recovery `while True` runs while still on the mirror map, where only `setting_assets.png` (~0.89) matches, so the gear is clicked forever until the ~90s stuck-guard kills the thread.
- Scope: `tasks.mirror.search_road.search_road_from_road_map`, `keyboard_node_fallback`, `Mirror.search_road` recovery loop.

### 2. Contracts

| Input / outcome | Contract |
| --- | --- |
| `identify_nodes()` returns `None`, or `bus` / `bus_pos` is `None` | `search_road_from_road_map()` returns `([], [])`; never raise. Empty path degrades to default/farthest fallback. |
| Recovery loop and `is_on_mirror_map(auto, use_ocr=False)` is true | Call `keyboard_node_fallback()` (arrow keys + `enter_assets` check); return `True` on entry, else `continue`. Do not fall through to the setting-gear click while on the map. |
| Not on the map (pause menu / window) | Keep the existing exit/re-enter logic (`to_window`, `setting`, forfeit). |
| `keyboard_node_fallback()` | Only press arrow keys; gated by the on-map check so mouse mode and non-map states are unaffected. |
| Re-enter buttons `to_window_assets` / `towindow&forfeit_confirm_assets` | Click at `threshold=0.7`, not the default 0.8. At 1600x900 `to_window` scores ~0.78 (verified in issue #893 debugLog); the default 0.8 gate makes the gear toggle the pause menu forever until the 90s stuck-guard. |

### 3. Tests Required

- `search_road_from_road_map()` returns `([], [])` when bus is missing and when `identify_nodes` is `None`, with no exception.
- `keyboard_node_fallback()` returns `True` when a node is entered and `False` when stuck.
- Structural: `Mirror.search_road` recovery calls `keyboard_node_fallback` under `is_on_mirror_map(auto, use_ocr=False)` before the `setting_assets.png` click.

## Common Mistakes

- Do not add a per-event “土偶/罪人” template merely because one result page failed; extend the shared OCR parser with an evidence-backed semantic boundary.
- Do not use `time.time()` for bounded UI waits that should ignore wall-clock adjustments; use `monotonic()`.
- Do not continue to team selection or `Battle.to_battle()` after an entry function returns `False`.
- Do not use “the choice page remained visible” as evidence that the first choice is disabled; only the current RGB/HSV button state authorizes selecting the second choice.
- Do not emit the normal completion toast or perform completion actions after a daily task returns `False`.
- Do not treat `shop_coins_assets.png` as shop entry. Map gold HUD can score ≥0.96; require map veto plus a shop-only control.
- Do not gate map-leave on `legend_assets` at the default 0.8; logged map legend is 0.777. Use `MAP_LEGEND_THRESHOLD` (0.75) or raw scores.
- Do not skip `search_road_farthest_distance()` when `background_click` is on, and do not raise `InputAttributeError` when scroll returns `False`.
- Do not feed a `None` from `identify_nodes()` (or a `None` bus) into `search_road_from_road_map` node math; return `([], [])` and let default/farthest fallback run.
- Do not click `setting_assets.png` in a loop while `is_on_mirror_map(use_ocr=False)`; use `keyboard_node_fallback()` so recovery does not depend on the 90s stuck-guard.
