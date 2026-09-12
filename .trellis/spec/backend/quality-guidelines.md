# Quality Guidelines

> Code quality standards for the Python automation layer.

## Overview

Automation behavior is a state machine over screenshots. New recognition paths must be bounded, testable without a live game, and unable to silently convert an unknown page into a navigation attempt.

## Required patterns

### Pure recognition boundaries

Place OCR-only parsing in a module that has no `Automation`, OCR engine, configuration, logging, sleep, or click dependency. Keep side effects in the caller.

```python
# Good: pure, importable in a lightweight test process.
def resolve_event_page(entries: list[OcrEntry]) -> EventPageResolution | None: ...

# Caller owns I/O and state changes.
resolution = resolve_event_page(auto.get_ocr_entries())
if resolution is not None and resolution.position is not None:
    auto.mouse_click(*resolution.position)
```

`tasks.event_page` is the current shared boundary for daily event OCR recognition. `tasks.event.event_handling` may re-export its public interface for compatibility, but new pure tests should import the lightweight module directly.

`tasks.mirror.shop_presence` is the shared boundary for mirror shop vs map. `resolve_mirror_shop_presence()` is pure; `inspect_mirror_shop_presence()` collects OCR texts and raw template scores (`get_image_match_score`, not `find_element` at 0.8) then calls the parser. `is_on_mirror_map()` is the shared map gate: legend at `MAP_LEGEND_THRESHOLD` first, OCR only as fallback. Battle and `back_init_menu` must pass `use_ocr=False`. Do not add this module to `tasks/mirror/__init__.py` — that file walks shop asset directories. All three `shop_coins` sites in `tasks/mirror/mirror.py` must call the same inspect helper.

### Bounded recovery

Every page-recovery loop needs an explicit authority for its timeout. If a specialized wait is longer than a general retry loop, the specialized monotonic timeout must keep the general budget from expiring first. A recovery retry count must be a named constant and shared across equivalent flows.

Windows game launch follows the same rule: `Game.start_game()` creates one pending request, and `init_game()` owns the `monotonic()` deadline while polling `screen.init_handle(start_if_missing=False)`. A poll must never independently re-open Steam. A pending request must be cleared on window success, launch timeout, and every game-close path.

### 商店离开恢复契约

- 触发：离店按钮持续命中却无页面推进，或截图持续失败。
- 签名：`resolve_shop_leave_dialog(entries) -> (visible, position | None)`；`Shop.in_shop()` 显式 `False` 表示失败。
- 契约：离店每轮先消耗预算，成功点击不能跳过计数。模板确认优先；OCR 需要离店标题与下方同行的取消/确认几何关系。
- 错误矩阵：地图证据→正常退出；标题有而确认不明确→等待且消耗预算；预算耗尽→`back_init_menu(allow_restart=False)`；恢复失败→`Mirror.in_shop()` 抛出任务错误，不吞掉失败。
- 示例：合法弹窗确认可点击；只有“确认”文字不可点击；弹窗存在时不点底层离开。
- 测试：`test_shop_leave_budget.py` 覆盖点击命中、截图失败、回地图、网络恢复失败及主页恢复结果；`test_shop_leave_dialog.py` 验证授权；`test_mirror_shop_failure.py` 验证包装层传播。
- 错误写法：`if click_leave(): continue` 放在计数前；正确写法：计数在所有 `continue` 之前。
- 主题包选择同样在截图和识别异常之前消耗预算，耗尽只恢复一次；`select_theme_pack()` 显式False必须阻止Mirror更新楼层计时。回归：`test_theme_pack_recovery_budget.py`、`test_theme_pack_failure_boundary.py`。
- `check_team()` 的至少5人候选必须覆盖总人数5–12，不能漏掉 `5/12` 或 `12/12`；参见 `test_team_survival_count.py`。

### Desktop dialog authorization

A desktop-wide OCR click has a stricter boundary than a game-window OCR click because unrelated windows share the frame. Keep its recognition parser pure and authorize a click only from a complete semantic **and geometric** dialog signature. For the authorized Steam cloud dialog, require all Chinese text anchors (`无法同步`, `未能将您的存档`, `Steam 云同步`, exact `仍然进行游戏`), a continuation button below the body, and a bounded shared dialog region. Consume the one allowed click attempt before invoking the desktop click API so a click exception cannot retry an irreversible action.

```python
# Good: one pending request and one authorized desktop confirmation attempt.
def handle_pending_launch(self) -> bool:
    if self._launch_requested_at is None or self._cloud_sync_confirmation_attempted:
        return False
    return handle_steam_cloud_sync_dialog(
        on_dialog_detected=lambda: setattr(self, "_cloud_sync_confirmation_attempted", True)
    )
```

### Template first, OCR second

Keep existing templates as the preferred recognition path. OCR fallback runs only after the relevant templates did not advance the page. A generic OCR keyword without enough page context is not a safe click target.

### Choice availability is a visual state, not a retry count

Daily event choices have an extra safety boundary: choose a second candidate only after the **first button itself** is confirmed grey in the RGB frame. `Automation.take_screenshot_with_color()` preserves RGB, so `is_first_event_choice_disabled()` may use `cv2.COLOR_RGB2HSV`. A persistent selection page is not evidence that the first option became unavailable.

```python
if is_first_event_choice_disabled(auto.color_screenshot, first_choice, choice_slot_spacing=spacing):
    auto.mouse_click(*second_choice)
else:
    # The first button is still usable: template first, then its OCR center.
    auto.click_element("event/select_first_option_assets.png") or auto.mouse_click(*first_choice)
```

Keep a named local retry limit (`EVENT_CHOICE_MAX_RETRY_ATTEMPTS`) for a stable selection page. It must terminate to `False`; it must not consume the event-result animation budget or reset the total battle timeout.

## Forbidden patterns

- **Do not** reset a total task timeout just because a UI animation is being waited on; reset only the local recognition budget when the state is known.
- **Do not** add per-event text/template branches for a common event transition. Extend the shared parser and its state table instead.
- **Do not** duplicate EXP and Thread recovery budgets. Use one helper and one named maximum.
- **Do not** put a pure parser behind a package initializer that eagerly imports the OCR runtime; this makes unit tests depend on a game runtime unnecessarily.
- **Do not** treat a failed entry recovery as permission to proceed to team selection or battle start.
- **Do not** use a one-time “first choice attempted” flag that makes a non-advancing choice page wait forever or changes selection to the second option without a grey-state observation.
- **Do not** flatten a terminal `False` into `None` at a battle, daily-group, startup-resume, or top-level task boundary.
- **Do not** make each missing-window poll launch Steam again; the launch request is state, not a retry loop iteration.
- **Do not** use a generic desktop OCR keyword or a fixed screen coordinate to click a Steam dialog; validate its complete same-region signature first.
- **Do not** force-kill the Windows game from individual recovery branches. Delegate to `Game.close_game()` so every caller shares normal-close waiting and the single timeout fallback.

## Testing requirements

Run project tests through the managed environment:

```bash
uv run pytest
uv run ruff check tasks/battle/battle.py tasks/event_page.py tasks/event/event_handling.py tasks/base/back_init_menu.py tasks/daily/luxcavation.py tasks/base/script_task_scheme.py tests --ignore E722
```

`E722` is an existing baseline exemption, not permission to introduce new lint failures.

For daily event changes, tests must include:

- a pure OCR parser test runnable without RapidOCR;
- behavior-driven mutation-sensitive coverage showing event `wait` and `advance` do not exhaust the local battle budget;
- a 40-second event animation path and a 60-second bounded timeout path;
- server-error priority over all normal OCR/page handling;
- both EXP and Thread’s one-recovery success/failure/renewal-failure/second-exhaustion paths;
- RGB/HSV grey-choice recognition at beta, 720p, and 900p candidate spacing; grey first choice must choose the second slot, enabled first choice must retry the first slot;
- bounded failure when selection OCR is absent or its valid target does not advance;
- daily failure propagation through a single battle, group, wrapper, startup-resume path, and top-level task runner (including no completion toast/action);
- original `from tasks.event import event_handling` singleton behavior when import order changes.

For Windows launch/Steam recovery changes, also test:

- a pure complete dialog match, each missing anchor, cancel-only dialog, a misplaced button, and anchors split across desktop regions;
- a pending launch does not repeat a Steam URL, including when the game process already exists but no game window is ready;
- a click exception consumes that request's single confirmation attempt;
- a full case-insensitive process-name match succeeds but a similarly named process does not;
- `WM_CLOSE` occurs before the only force-kill fallback, and all Windows close wrappers delegate to `Game.close_game()`;
- unrelated top-level task tests stub image recognition instead of reading real windows, screenshots, or processes.

## Code review checklist

- Is a new state recognized by a pure semantic parser when it is shared by battle and recovery flows?
- Are every click target and `None`/timeout outcome checked before side effects?
- Can a general loop budget preempt a documented longer animation wait?
- Does a new fallback run after server-error handling and after existing template matches?
- Did the implementation preserve group-level navigation rather than adding an unconditional per-battle return home?
