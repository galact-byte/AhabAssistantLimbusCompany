# 上游开放 Issue 适用性核对

范围：209条开放报告按正文症状与当前模块聚类核对；不是209项实机复现或全附件审计。分类完成，证据不足是审核结论而非证明不存在。混合功能请求不自动排除其缺陷描述。

| Issue | 标题 | 状态 | 依据/边界 |
|---|---|---|---|
| [#905](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/905) | [Bug] 选择队伍时会把上边的编队拖到下方 | 上游相关修复已融合，实机待验 | cae50bf MuMu起拖/惯性修正；报告版本1.5.1 |
| [#904](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/904) | [Bug] 第二层战斗自动失败卡退 | 相关逻辑缺陷已修，实机根因未定 | check_team漏掉10–12人总数；不代表复现报告环境 |
| [#902](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/902) | [Feature] 打开aalc后自动开始运行 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#900](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/900) | [Bug] 在第五层出现道中战斗结束后显示队伍成员团灭然后自动退出镜牢 | 相关逻辑缺陷已修，实机根因未定 | check_team漏掉10–12人总数；test_team_survival_count |
| [#898](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/898) | 模拟器启动加载识别为未进入主菜单导致反复重开 | 环境或证据不足 | 模拟器/显示环境：module/automation及game_and_screen；需对应Windows/MuMu/显示环境，未改驱动或下载模拟器 |
| [#896](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/896) | [Bug] 普牢第五层通过领取奖励后报错 | 上游相关修复已融合，实机待验 | 40283e0结算等待加载；仍需真实结算验证 |
| [#888](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/888) | [Bug] MUMU模拟器更新至V6.5.8后AALC无法识别安卓15 | 上游相关修复已融合，环境待验 | mumu_control.py支持12.0/15.0 DLL候选路径 |
| [#885](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/885) | 选错编队 | 上游相关修复已融合，实机待验 | b20e1e8及40队定位；保留命名精确匹配 |
| [#875](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/875) | [Bug] 输入issue标题 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#874](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/874) | [Feature] 定向卡包功能 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#866](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/866) | [Feature] 自定义小指良守备回合数 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#857](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/857) | [Feature] 网络波动时不会去点击弹窗，仍然直接点击游戏 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#850](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/850) | [Bug] 测试版一直显示 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#849](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/849) | [Bug] 20 区的奇迹，设置了权重为 0，但是依旧优先选择 | 证据不足 | 当前按最大权重选择；负权重不等于禁选，需报告帧与配置确认OCR及权重映射 |
| [#846](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/846) | 模拟器连接问题 | 上游相关修复已融合，环境待验 | 4471760；缺少同版本MuMu复现环境 |
| [#844](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/844) | [Bug] 最新测试版中镜牢寻路在执行之前会弹出设置框导致AALC进程卡死无法进行。 | 本地已有回归保护 | test_mirror_search_road_recovery：地图内键盘恢复与重进门限 |
| [#842](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/842) | [Bug] 用软件将084字体更改后，自动打镜牢内选完人格后卡在选择界面上，无法开始战斗 | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#832](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/832) | [Bug] 在选队的过程中滑动过快选到了别的队伍 | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#827](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/827) | [Bug] 概率会卡在钮本这里不执行 | 环境或证据不足 | 日常/换体：tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行 |
| [#826](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/826) | [Feature] 输入issue标题 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#825](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/825) | [Feature] MUMU15.0支持 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#820](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/820) | [Bug] 普通与困难镜牢无法正常切换 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#819](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/819) | 寻路逻辑有误，寻路时间过长 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#815](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/815) | 等待页面执行镜牢寻路 | 环境或证据不足 | 主题包/寻路：select_theme_pack.py/search_road.py；权重与空识别保护有测试，原始识别帧不可用 |
| [#814](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/814) | 等待页面执行镜牢寻路 | 环境或证据不足 | 主题包/寻路：select_theme_pack.py/search_road.py；权重与空识别保护有测试，原始识别帧不可用 |
| [#810](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/810) | [Bug] 通过进程判断游戏运行错误 | 本地已有回归保护 | test_steam_cloud_recovery：进程名称完整匹配/窗口轮询 |
| [#800](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/800) | [Bug] 队伍设置自动勾选忽略商店 | 上游相关修复已融合 | Mirror构造函数model_copy(deep=True)，不再共享原配置列表 |
| [#799](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/799) | [Bug] 困牢饰品选择卡死 | 环境或证据不足 | 商店/饰品：tasks/mirror/in_shop.py；策略受队伍配置和饰品模板影响，不能仅按标题更改购买/合成偏好 |
| [#796](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/796) | [Bug] 经常/偶发性卡死和重启失效 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#795](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/795) | [Bug] 不是什么特别严重的问题 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#794](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/794) | [Bug] 镜牢无法观测饰品 | 环境或证据不足 | 商店/饰品：tasks/mirror/in_shop.py；策略受队伍配置和饰品模板影响，不能仅按标题更改购买/合成偏好 |
| [#793](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/793) | 關於正常運行一段時間後，會出現圖片無法識別情況(偶然出現) | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#792](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/792) | [Bug] 关于无良夜的镜牢问题 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#791](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/791) | [Bug] 困牢打开花男会无限打开罪人buff栏，无法正常进行战斗 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#789](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/789) | [Bug] 合成会合掉良秀专武，疑似bug | 环境或证据不足 | 商店/饰品：tasks/mirror/in_shop.py；策略受队伍配置和饰品模板影响，不能仅按标题更改购买/合成偏好 |
| [#787](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/787) | [Bug] MuMu模拟器6.0适配 | 环境或证据不足 | 模拟器/显示环境：module/automation及game_and_screen；需对应Windows/MuMu/显示环境，未改驱动或下载模拟器 |
| [#786](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/786) | [Feature] 增加每日换体力的次数的上限 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#785](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/785) | [Feature] 新功能建议 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#782](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/782) | [Bug] 进入战斗之前会卡死在编队界面 | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#779](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/779) | [Feature] 普牢进入经验记忆，然后一直卡在林庆业 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#778](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/778) | 偶发性bug：执行“领取奖励”时，游戏窗口左右漂移并重复执行动作“点击邮箱图标” | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#773](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/773) | 想用小蓝良速刷，观测时候选择不到蜘蛛丝 | 环境或证据不足 | 商店/饰品：tasks/mirror/in_shop.py；策略受队伍配置和饰品模板影响，不能仅按标题更改购买/合成偏好 |
| [#771](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/771) | [Bug] 无人值守情况下，镜牢关卡长时间未通关导致一直重置游戏 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#770](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/770) | [Feature] 体力换饼独立功能 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#768](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/768) | [Feature] 输入issue标题 新增技能替换多选 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#767](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/767) | 用模拟器刷牢时出现的一些小问题 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#766](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/766) | 无法正确观测呼吸体系饰品，会跳到沉沦中去 | 环境或证据不足 | 商店/饰品：tasks/mirror/in_shop.py；策略受队伍配置和饰品模板影响，不能仅按标题更改购买/合成偏好 |
| [#765](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/765) | [Bug] 模拟器会在选择队伍时会拖动并改变队伍顺序 | 上游相关修复已融合，实机待验 | cae50bf；不以标题判定已根治 |
| [#752](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/752) | [Bug] 模拟器无限重启游戏 | 环境或证据不足 | 模拟器/显示环境：module/automation及game_and_screen；需对应Windows/MuMu/显示环境，未改驱动或下载模拟器 |
| [#747](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/747) | [Feature] 自定义返回主界面任务超时时间 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#745](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/745) | [Bug] 商店会购买白棉花 | 环境或证据不足 | 商店/饰品：tasks/mirror/in_shop.py；策略受队伍配置和饰品模板影响，不能仅按标题更改购买/合成偏好 |
| [#744](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/744) | [Bug] 事件不能进行 一直卡在选择roll点之前的页面 | 环境或证据不足 | 事件：tasks/event_page.py、battle.py；事件恢复回归通过，具体事件帧未提供则不认定同根因 |
| [#743](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/743) | [Feature] 合成会用掉良秀专武 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#741](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/741) | [Feature] 守备问题（指良秀&中指队） | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#740](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/740) | [Feature] 引入 regression test 流程，保障新版本稳定性 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#737](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/737) | [Bug] 无法自动启动游戏 | 环境或证据不足 | 启动/退出/定时：script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump |
| [#736](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/736) | [Bug] 罪人编队阶段无响应 | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#735](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/735) | [Bug] 输入issue标题 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#734](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/734) | 已知问题清单，发新 issue 时请看这 | 问题汇总，不作为单一缺陷 | 包含多项不同状态；不能以勾选或关闭状态证明修复 |
| [#733](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/733) | 不能调连续战斗 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#730](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/730) | 希望刷牢有无限守备；合成4级饰品/楼层达到X层后，改变战斗策略的选项。 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#717](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/717) | [Bug] 无限体力换饼，无法进入下一步 | 环境或证据不足 | 日常/换体：tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行 |
| [#715](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/715) | [Feature]希望在刷牢里加个无限守备 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#714](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/714) | [Feature]希望在刷牢里加个无限守备 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#713](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/713) | [Bug] 镜牢事件里进行判定时会卡死 | 环境或证据不足 | 事件：tasks/event_page.py、battle.py；事件恢复回归通过，具体事件帧未提供则不认定同根因 |
| [#711](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/711) | [Bug] 无法离开镜牢商店 | 本地证实并修复 | 离店点击绕过预算；test_shop_leave_budget / test_shop_leave_dialog |
| [#710](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/710) | [Bug] 纽本连续作战失效 | 环境或证据不足 | 日常/换体：tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行 |
| [#705](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/705) | [Bug] 可能是恶性bug-进入战斗过程中直接卡死退出 | 环境或证据不足 | 启动/退出/定时：script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump |
| [#704](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/704) | 综合问题 内附链接 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#702](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/702) | [Bug] 关闭键盘寻路后编队无法正确识别人格 | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#701](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/701) | 自动编队问题 | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#700](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/700) | [Feature] 请求加入教程界面的相关自动处理 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#699](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/699) | [Bug] 勾选使用键盘来进行镜牢寻路时进入牢内就不动了 | 环境或证据不足 | 主题包/寻路：select_theme_pack.py/search_road.py；权重与空识别保护有测试，原始识别帧不可用 |
| [#696](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/696) | 程式打不开 (已解决) | 环境或证据不足 | 启动/退出/定时：script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump |
| [#695](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/695) | 希望能加个饰品观测的功能 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#692](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/692) | [Feature] aalc貌似不能连接windows子系统 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#690](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/690) | [Bug] 今天更新完游戏清日常好像不能连续作战了 | 环境或证据不足 | 日常/换体：tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行 |
| [#687](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/687) | [Bug] 5/28更新后勾选“使用键盘进行镜牢寻路”会导致反复开始结束寻路引起卡死 | 环境或证据不足 | 主题包/寻路：select_theme_pack.py/search_road.py；权重与空识别保护有测试，原始识别帧不可用 |
| [#686](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/686) | 刷普牢不会走问号多的路线 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#685](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/685) | [Bug] 输入issue标题 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#679](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/679) | 饰品观测 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#678](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/678) | 希望能增加［商店购买商品的种类选择］ | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#676](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/676) | [Bug] 宝宝，今天更新之后怎么没有语言选项了。模拟器英文一直显示是中文，然后无限换体力。 | 环境或证据不足 | 事件：tasks/event_page.py、battle.py；事件恢复回归通过，具体事件帧未提供则不认定同根因 |
| [#668](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/668) | [Bug] 镜牢编队及商店bug | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#667](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/667) | [Feature] 希望能在狂气换体时每换一次加个返回主界面 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#662](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/662) | [Bug] 新功能语言检测出错 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#660](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/660) | 建议增加开局观测饰品的功能 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#659](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/659) | [Bug] 镜牢设置编队名称每次打开AALC都会恢复成以前的设置 | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#648](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/648) | [Bug] 进入镜牢异常 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#645](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/645) | [Bug] 镜牢特定事件出现卡死 | 环境或证据不足 | 事件：tasks/event_page.py、battle.py；事件恢复回归通过，具体事件帧未提供则不认定同根因 |
| [#642](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/642) | Mac电脑无法直接exe使用 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#640](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/640) | [Bug] 无法进入镜牢 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#639](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/639) | [Feature] 关于战斗开始前由于网络问题而卡在“服务器发生错误。请稍后再试。”弹窗界面死锁的问题解决建议 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#637](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/637) | [Bug] 进入镜牢异常 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#636](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/636) | [Feature] 每周困牢加成和定时任务使用的冲突问题 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#635](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/635) | 希望在模拟器上的任务卡死识别能更加智能 | 相关恢复缺陷已修，模拟器冻结未复现 | 截图失败与识别异常统一有限预算；不能证明能解除模拟器自身冻结 |
| [#634](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/634) | [Bug] 镜牢-多选一饰品时 无法识别已拥有饰品 | 环境或证据不足 | 商店/饰品：tasks/mirror/in_shop.py；策略受队伍配置和饰品模板影响，不能仅按标题更改购买/合成偏好 |
| [#633](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/633) | [Bug] UI界面字体异常 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#630](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/630) | [Bug] 输入issue标题 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#625](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/625) | [Bug] 琥珀色的黄昏卡包专属事件-去往休息的选项 | 环境或证据不足 | 主题包/寻路：select_theme_pack.py/search_road.py；权重与空识别保护有测试，原始识别帧不可用 |
| [#623](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/623) | 五层商店暂停 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#620](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/620) | [Bug] 无法合成脑啡肽模块 | 环境或证据不足 | 商店/饰品：tasks/mirror/in_shop.py；策略受队伍配置和饰品模板影响，不能仅按标题更改购买/合成偏好 |
| [#616](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/616) | [Bug] 路径管理器初始化存在问题 | 环境或证据不足 | 主题包/寻路：select_theme_pack.py/search_road.py；权重与空识别保护有测试，原始识别帧不可用 |
| [#615](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/615) | [Bug] 脚本无法运行 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#612](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/612) | [Bug] 更新1.4.9后，纺锤本连续战斗选取五级本而不是六级 | 环境或证据不足 | 日常/换体：tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行 |
| [#598](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/598) | 麻烦改进一下饰品运营的思路 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#594](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/594) | [Bug] 使用MUMU模擬器時,一進螢幕保護程式就無法選取卡包 | 相关逻辑缺陷已修，原环境未复现 | 主题包识别异常continue绕过预算；新增theme_pack_recovery_budget测试，字符串权重实机来源未定 |
| [#586](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/586) | [Feature] 监听并拦截py32模拟信号，同时通过罗技驱动转换为物理鼠标信号输出 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#585](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/585) | [Feature] 希望修改输入模式，以避免最新limbus的检测。 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#579](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/579) | [Feature] 希望增加跳过纺锤本的功能 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#575](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/575) | [Feature] 关于困牢每一层最后一关的饰品选择策略优化 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#574](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/574) | [Bug] 自动战斗p问题 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#572](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/572) | 事件的选项选不了了 | 环境或证据不足 | 事件：tasks/event_page.py、battle.py；事件恢复回归通过，具体事件帧未提供则不认定同根因 |
| [#570](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/570) | [Feature] 能不能在自动镜牢出个战斗爽选项 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#568](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/568) | [Bug] 4.2镜牢事件UI更新了，AALC会卡在新UI上面 | 环境或证据不足 | 事件：tasks/event_page.py、battle.py；事件恢复回归通过，具体事件帧未提供则不认定同根因 |
| [#567](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/567) | [Bug] 部分操作不能正常运行 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#566](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/566) | [Bug] 镜牢编队时排版出错 | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#564](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/564) | [Feature] 鏡牢選配隊加入從下往上的功能 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#563](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/563) | AALC自动关闭 | 环境或证据不足 | 启动/退出/定时：script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump |
| [#562](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/562) | [Bug] 纽本不正常打开 | 环境或证据不足 | 日常/换体：tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行 |
| [#561](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/561) | [Bug] 编队成员无法上场 | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#557](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/557) | 定时启动设置5：05启动，运行到7：00就直接关闭AALC,而边狱巴士没有关闭 | 环境或证据不足 | 启动/退出/定时：script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump |
| [#556](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/556) | [Feature] 希望加入合成不消耗星芒选项 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#555](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/555) | [Feature] 关于目前流出代码的一些易于实现反作弊建议 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#553](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/553) | [Bug] 出售饰品，无法点击确认 | 环境或证据不足 | 商店/饰品：tasks/mirror/in_shop.py；策略受队伍配置和饰品模板影响，不能仅按标题更改购买/合成偏好 |
| [#551](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/551) | [Bug] 在困难镜牢超长线战斗中，AALC会认为游戏卡死并推出 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#550](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/550) | 希望加入十层自动坐牢功能 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#545](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/545) | 希望加入长时间卡死自动结束任务 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#538](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/538) | 希望能追加完成日常任務一次後再關機 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#537](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/537) | [Bug] 一直卡在换体力步骤 | 环境或证据不足 | 日常/换体：tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行 |
| [#536](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/536) | 希望能在坐牢设置里添加使用镜牢的租赁队伍的选项 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#533](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/533) | [Bug] 笔记本锁屏后无法运行 | 环境或证据不足 | 模拟器/显示环境：module/automation及game_and_screen；需对应Windows/MuMu/显示环境，未改驱动或下载模拟器 |
| [#529](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/529) | [Bug] 点击开始后一直点击左上角 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#528](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/528) | [Bug] 新活動卡包900秒卡死 | 环境或证据不足 | 主题包/寻路：select_theme_pack.py/search_road.py；权重与空识别保护有测试，原始识别帧不可用 |
| [#525](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/525) | [Bug] 日常任务执行出错 | 环境或证据不足 | 日常/换体：tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行 |
| [#524](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/524) | [疑問] AALC編隊介面儲存按鈕丟失 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#522](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/522) | [Bug] 狂气换体功能bug | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#518](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/518) | [Bug] 镜牢的定向刷新失效了 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#517](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/517) | [feature]AALC应该识别气泡文本 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#515](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/515) | [Bug] 定时执行 的一系列BUG反馈 | 环境或证据不足 | 启动/退出/定时：script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump |
| [#514](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/514) | [Bug] 战斗过程中报错后中止 | 环境或证据不足 | 启动/退出/定时：script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump |
| [#512](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/512) | [Bug] 定时执行AALC功能失效 | 环境或证据不足 | 启动/退出/定时：script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump |
| [#511](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/511) | [Feature] 战斗胜利应该自动点击屏幕 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#505](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/505) | [Bug] mumu模拟器牢内编队画面无法点击To battle | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#503](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/503) | [Bug] 新版本在窗口失去响应时不会自动重启 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#500](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/500) | [Bug] 窗口设置为无限制之外的情况下无法使用 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#499](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/499) | [Bug] 无法自动启动游戏 | 环境或证据不足 | 启动/退出/定时：script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump |
| [#497](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/497) | [Bug] 启动AALC.exe报错 | 环境或证据不足 | 启动/退出/定时：script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump |
| [#495](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/495) | [Bug] 一直在返回主界面 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#493](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/493) | [Bug] 主頁面要進入打地牢，但完全無動作 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#492](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/492) | [Bug] 牢內的戰鬥畫面進入畫面，不會按戰鬥按鈕 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#491](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/491) | [Bug] UI更新后无法正常识别 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#490](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/490) | [Feature] 主页功能顺序可排列 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#488](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/488) | 关于合成设置的问题 | 环境或证据不足 | 商店/饰品：tasks/mirror/in_shop.py；策略受队伍配置和饰品模板影响，不能仅按标题更改购买/合成偏好 |
| [#487](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/487) | 脚本的自动换体力工具无法正常循环 | 环境或证据不足 | 日常/换体：tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行 |
| [#485](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/485) | 屏幕分辨率问题 | 环境或证据不足 | 模拟器/显示环境：module/automation及game_and_screen；需对应Windows/MuMu/显示环境，未改驱动或下载模拟器 |
| [#483](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/483) | 关于一些机制怪的简易应对 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#477](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/477) | [Feature] 关于主题包权重问题 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#474](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/474) | [Feature] 优化定时执行aalc | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#473](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/473) | [Bug] 识别屏幕无法正常运行 | 环境或证据不足 | 模拟器/显示环境：module/automation及game_and_screen；需对应Windows/MuMu/显示环境，未改驱动或下载模拟器 |
| [#472](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/472) | [Feature] 希望自动战斗在牢内识别速度能够提高 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#471](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/471) | Failed to upload to MirrorChyan for KIYI671/AhabAssistantLimbusCompany | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#467](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/467) | 模拟器镜牢寻路卡死 | 环境或证据不足 | 主题包/寻路：select_theme_pack.py/search_road.py；权重与空识别保护有测试，原始识别帧不可用 |
| [#464](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/464) | [Feature] 能否在小工具栏加上一键刷取ex饰品的功能 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#463](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/463) | [Feature] 希望能增加对多显示器的兼容 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#462](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/462) | [Feature] 希望能使用標籤編隊名稱 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#444](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/444) | [Bug] 战斗途中更改为无限守备不起作用 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#440](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/440) | 事件选人会卡住 | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#438](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/438) | [Bug] 运行到镜牢商店结束时无法正常结算 | 本地证实并修复 | 同离店循环；原日志10:50–12:37；未证明像素失配原因 |
| [#437](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/437) | [Bug] 选择队伍 | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
| [#433](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/433) | [Feature] 希望经验本可以选择首回合守备 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#430](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/430) | [Feature] 关于镜牢寻路的优化建议：路径选择优化 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#429](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/429) | [Bug] 大量报错，导致电脑卡死 | 环境或证据不足 | 启动/退出/定时：script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump |
| [#427](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/427) | 笔记本在关闭盖子后不再工作（已经调整关闭盖子后策略） | 环境或证据不足 | 模拟器/显示环境：module/automation及game_and_screen；需对应Windows/MuMu/显示环境，未改驱动或下载模拟器 |
| [#422](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/422) | [Bug] 无法正确识别MUMU模拟器的边狱巴士 | 环境或证据不足 | 模拟器/显示环境：module/automation及game_and_screen；需对应Windows/MuMu/显示环境，未改驱动或下载模拟器 |
| [#418](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/418) | [Bug] AALC无法启动游戏 | 环境或证据不足 | 启动/退出/定时：script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump |
| [#416](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/416) | [Feature] 支持Linux | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#407](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/407) | 我希望新增君主宝能够在非链接战第一回合使用守备技能功能 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#402](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/402) | [Bug] 在“驾驶席”页面卡住 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#391](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/391) | [Feature] 关于星光10的3级饰品选择问题 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#388](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/388) | 疑似旧版本config不能适配新脚本，导致exe无法打开 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#387](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/387) | [Feature] 关于鼠标的问题 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#386](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/386) | 在解锁并首次通关过50级纽本的情况下脚本仍会选择30级纽本 | 环境或证据不足 | 日常/换体：tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行 |
| [#376](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/376) | [Feature] 求速刷普牢配队和设置推荐 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#375](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/375) | [Bug] 偶发的config内字符不可见导致程序无法运行现象 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#369](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/369) | [Feature] 希望AALC可以多开 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#353](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/353) | [Feature] 更轻松的选择卡包 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#347](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/347) | [Feature] 单独的一键体力换饼功能／定时换饼 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#341](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/341) | 不断重进镜牢 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#340](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/340) | [Feature] 输入issue标题 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#331](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/331) | [Bug] 使用管理员运行后依旧出错 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#330](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/330) | [Bug] 无限守备失效 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#327](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/327) | [Bug]打开应用后没有显示 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#324](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/324) | [Feature] 定时启动 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#315](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/315) | [Bug] 纽本只能进行一次，然后在主界面和进本界面循环 | 环境或证据不足 | 日常/换体：tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行 |
| [#307](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/307) | [Bug] 镜牢截图出错 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#302](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/302) | [Bug] UI 布局错乱导致控件不可见/重叠 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#301](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/301) | [Feature] 增加开机自启动 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#283](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/283) | [Bug] 普牢无法自动合成饰品 | 环境或证据不足 | 商店/饰品：tasks/mirror/in_shop.py；策略受队伍配置和饰品模板影响，不能仅按标题更改购买/合成偏好 |
| [#278](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/278) | [Feature] 希望增加“在激进合成时忽略体系饰品”的设置 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#275](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/275) | [Feature] 希望出个普牢在5层刷活动卡包时能切换为困牢的功能 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#274](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/274) | [Bug] 刷牢多体系轮换问题 | 环境或证据不足 | 报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值 |
| [#268](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/268) | [Feature]希望优化饰品升级优先级 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#263](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/263) | [Bug] 日常经验本、纽本战斗到一半会中断 | 环境或证据不足 | 日常/换体：tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行 |
| [#253](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/253) | [Feature] 希望可以优化卡包结束后的饰品三选一选择逻辑 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#249](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/249) | [Feature] 增加“自定义商店刷新次数”选项 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#218](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/218) | [Feature] 更多合成自定義 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#116](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/116) | [Feature] 关于镜牢商店逻辑和功能的建议 | 功能请求初筛 | 不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除 |
| [#19](https://github.com/KIYI671/AhabAssistantLimbusCompany/issues/19) | 讨论下现版本用AALC刷镜5的话，哪个队伍最效率呢？ | 环境或证据不足 | 编队：tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题 |
