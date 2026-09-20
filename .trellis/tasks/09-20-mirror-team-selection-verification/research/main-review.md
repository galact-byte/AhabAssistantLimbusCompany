# 主会话审查与复验

## 审查修正
遵循用户全局10.0要求，后续审查和修正均主会话直接执行，未再派代理。
发现初稿每次扫描40槽、短列表失败、无关远端重名阻止选第二项。先补测试得到4 failed/25 passed（main-red-navigation.txt），再改为按需导航；本报告覆盖implementation-report.md中已过期的40槽策略。

- 按顺序：观察归顶后下滚一次并回顶确认输入有效，仅扫描至目标；按实际行间重叠计数，不推算滚轮像素。
- 按编号：当前页唯一命中可直接核验，不需要归顶；未命中再归顶并扫描。
- 仅检查经过页面的重名/歧义；不为检查远端重名强制遍历整表。当前页有重复仍拒绝。
- 测试新增12槽选第二项、不超过8次滚动、当前页按编号不滚动、向上输入单向失效不冒充顶部。
- 亲自核查输入差异、客户端/屏幕坐标、Automation反射交互门、纯解析数据形状与镜牢/日常失败传播。

## 最终验证
- `.venv/Scripts/python.exe -m pytest tests -q`：307 passed in 13.64s，输出main-regression.txt。
- `.venv/Scripts/python.exe -m ruff check module/automation/input_handlers/input.py tasks/team_list.py tasks/teams/team_formation.py tests --ignore E722`：All checks passed。
- compileall覆盖3产品文件及3新增测试，通过；git diff --check通过（仅LF/CRLF提示）。
- 已更新quality-guidelines.md和CHANGES.md；未操作真实游戏、未修改配置、未覆盖发行目录、未提交/发布。

## 仍待验收
1600×900后台实际滚轮响应、完整页面定位/选中标题区域、模拟器与长期运行尚未验证。当前短列表全部可见且按顺序模式无法滚动时会保守失败，因为缺少首项锚点；按编号当前页明确命中不需要滚动。非标准布局、长名称分行、重名识别可能保守失败。此次测试证明危险左键拖动已从Windows编队滚动路径移除，不证明历史重排已在实机复现。

## 提交边界
仅本次产品文件、3新增测试、CHANGES、quality-guidelines和本任务目录；09-05/09-12/09-13既有未跟踪任务不纳入。按3.4等待用户一次性提交确认；不推送。任务保持in_progress，不能以单元测试代替实机验收归档。
