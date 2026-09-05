# 镜牢寻路 ONNX None 与重进死循环修复

来源：GitHub issue KIYI671/AhabAssistantLimbusCompany#893（本人 galact-byte 提交，AALC V1.5.2-beta.65，1600x900 Steam）。

## 问题

无限镜牢 + 键盘寻路（`mirror_keyboard_navigation` 开、`mirror_keyboard_simple_pathfinding` 关）时：

1. **ONNX 返回 None 带崩整轮寻路**：`identify_nodes()` 无检测时返回 `None`，`search_road_from_road_map()` 直接把 `None`（以及可能为 `None` 的 `bus`）喂给 `divide_the_area_by_y` / `bus[0]`，抛 `TypeError`，被 `search_road` 的 try 吞掉，road_map 规划整轮作废。
2. **重进镜牢死点齿轮**：`search_road` 末尾 `while True` 恢复循环里，脚本其实仍停在镜牢地图上，只有右上角设置齿轮 `setting_assets.png`（~0.89）命中，被反复空点，直到 ~90s 卡死保护 `back_init_menu` 杀线程，无限镜牢仅完成 1 层即停。

## 验收标准

- ONNX/`identify_nodes` 返回 None 或 `bus` 未定位时，`search_road_from_road_map()` 返回空路径（`[], []`）而不抛异常，寻路自然回退到 default/farthest 兜底。
- `search_road` 的重进恢复循环在检测到「仍在镜牢地图上」（`is_on_mirror_map(use_ocr=False)`）时，改走键盘方向键选节点并尝试进入，不再空点设置齿轮；不在地图上时保持原有退出/重进逻辑。
- 键盘兜底只在地图上触发（legend>=0.75 强信号），对鼠标模式与非地图状态无副作用。
- 新增回归测试覆盖：None 兜底返回空路径不抛异常、键盘兜底进节点成功/失败分支。
- `uv run pytest`、`ruff check`、`compileall` 全绿。

## 日志验证（debugLog.log，issue #893 附件原件）

拉取了 issue #893 附的 debugLog.log（后台模式 `background_click: True`、`win_input_type: background`、`set_win_size: 900`、`mirror_keyboard_navigation: True`、`mirror_keyboard_simple_pathfinding: False`），看到关键事实：

- 23:00—00:01 键盘寻路（`search_road.py:56 通过键盘按键寻路: M/D/U`）一直正常，跑完一个完整镜牢（层、战斗、商店、奖励卡、主题包均 OK）。
- 00:02:09 `mirror.py:1108 寻路出错, 尝试重进镜牢` 后进入重进恢复循环，之后持续振荡：`to_window_assets`（回到窗口）**0.78 / 0.21 交替**，`setting_assets`（齿轮）**恒 0.89 被点**。因 0.78 < 默认 0.8 门限，“回到窗口”永远点不上，齿轮反复开关暂停菜单。
- 00:03:19 `retry.py:127 已卡死70秒` → 00:03:24 重置窗口、终止脚本线程，`已完成普通镜牢进度 1 / 9999`。

**真正根因**：重进恢复分支里 `to_window_assets` 在 1600x900 实测 0.78，卡在默认 0.8 门限下方——与 legend 0.777（记忆 #402）同一类“近下阈”问题。已把 `to_window` 与 `towindow&forfeit_confirm` 的点击门限降到 0.7。

**分辨率/拖动附带结论**：真实地图帧上 legend 得分 **0.94**（清晰），说明 640x480 显示并未拖垮识别；启动时“渲染比例低”警告未触发（renderingScale≠低）。“无法拖动”是后台模式 + 工具为防误触把窗口改成无边框固定（`reduce_miscontact` 移除 WS_THICKFRAME/WS_CAPTION）所致的手动体验，不是坐标/识别 bug，属游戏端显示设置。

## 非目标

- 不改 ONNX 模型本身，也不改 1600x900 无法拖动/640x480 的分辨率问题（属另一独立现象，本次不处理）。
- 不触碰 `09-05-mirror-shop-false-positive` 商店误判链路。
