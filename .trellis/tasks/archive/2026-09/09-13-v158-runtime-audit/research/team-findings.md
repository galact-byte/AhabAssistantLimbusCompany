# 二队配置与实际游戏队伍映射

## 已确认
- `G:/BaiduNetdiskDownload/AALC_v1.5.8/AALC/logs/debugLog.log.6:52`：02:41:39 活动队列改为 `[2]`，`:3293` 03:17:39 开始镜牢仍为 `[2]`。不是勾选二队被忽略。
- `debugLog.log:4` 的配置快照：方案1「黑兽」team_number=1、team_system=3；方案2「蛛巢」team_number=1、team_system=0；活动队列=[2]；select_team_by_order=True。
- `tasks/base/script_task_scheme.py:365–378` 从队列取2，并传 `cfg.config.teams['2']` 给镜牢。
- `tasks/mirror/mirror.py:55` 将方案内部 team_number 作为游戏编队编号；`:1033` 调用 select_battle_team(self.team_number)。因此第二份方案的目标仍是游戏列表第1队。
- `tasks/teams/team_formation.py:161–179` 按顺序点击第num队，日志“成功找到队伍”发生在点击后，没有截图复核，不能单独证明选择成功；但本次传入的目标确实是1。
- `debugLog.log.6:3506` 03:18:15、`:15169` 04:12:10 等镜牢选队都记录 #1；`:14972` 记录 burn 体系，与方案2的体系吻合。
- `app/team_setting_card.py:127` 的“选择队伍名称”绑定 team_number；在按顺序模式下实际含义是游戏列表序号，并非 AALC 方案编号。

## 判断与边界
本次现象首先是“第二份自动化方案映射到游戏第1队”，不是队列执行了方案1。要用游戏第2队，应在第二份方案内部将游戏队伍目标设为2；本轮没有替用户修改配置。不应全局把方案ID强行等同游戏编队ID，否则破坏多方案复用同一编队的现有行为。

可选后续：明确显示“方案2 → 游戏第1队”，将选队日志改为目标与实际确认分离。涉及UI需独立批准范围并加载UI规范；不是本轮必须改动。
