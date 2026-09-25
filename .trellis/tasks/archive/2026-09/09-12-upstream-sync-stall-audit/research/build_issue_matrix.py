"""生成可追溯初筛表；未深入验证的报告明确保留证据不足。"""
import json
from pathlib import Path

root = Path(__file__).parent
issues = [i for page in json.loads((root / "upstream-open-issues.json").read_text(encoding="utf-8")) for i in page if "pull_request" not in i]
verified = {
    711: ("本地证实并修复", "离店点击绕过预算；test_shop_leave_budget / test_shop_leave_dialog"),
    438: ("本地证实并修复", "同离店循环；原日志10:50–12:37；未证明像素失配原因"),
    900: ("相关逻辑缺陷已修，实机根因未定", "check_team漏掉10–12人总数；test_team_survival_count"),
    904: ("相关逻辑缺陷已修，实机根因未定", "check_team漏掉10–12人总数；不代表复现报告环境"),
    905: ("上游相关修复已融合，实机待验", "cae50bf MuMu起拖/惯性修正；报告版本1.5.1"),
    765: ("上游相关修复已融合，实机待验", "cae50bf；不以标题判定已根治"),
    885: ("上游相关修复已融合，实机待验", "b20e1e8及40队定位；保留命名精确匹配"),
    896: ("上游相关修复已融合，实机待验", "40283e0结算等待加载；仍需真实结算验证"),
    888: ("上游相关修复已融合，环境待验", "mumu_control.py支持12.0/15.0 DLL候选路径"),
    846: ("上游相关修复已融合，环境待验", "4471760；缺少同版本MuMu复现环境"),
    800: ("上游相关修复已融合", "Mirror构造函数model_copy(deep=True)，不再共享原配置列表"),
    810: ("本地已有回归保护", "test_steam_cloud_recovery：进程名称完整匹配/窗口轮询"),
    844: ("本地已有回归保护", "test_mirror_search_road_recovery：地图内键盘恢复与重进门限"),
    849: ("证据不足", "当前按最大权重选择；负权重不等于禁选，需报告帧与配置确认OCR及权重映射"),
    734: ("问题汇总，不作为单一缺陷", "包含多项不同状态；不能以勾选或关闭状态证明修复"),
}
verified[594] = ("相关逻辑缺陷已修，原环境未复现", "主题包识别异常continue绕过预算；新增theme_pack_recovery_budget测试，字符串权重实机来源未定")
verified[635] = ("相关恢复缺陷已修，模拟器冻结未复现", "截图失败与识别异常统一有限预算；不能证明能解除模拟器自身冻结")
groups = [
    ("编队", ["编队", "队伍", "人格", "选人"], "tasks/teams/team_formation.py；test_team_name_selection；缺对应帧/滚动环境不能排除定位问题"),
    ("主题包/寻路", ["卡包", "主题", "寻路", "路径"], "select_theme_pack.py/search_road.py；权重与空识别保护有测试，原始识别帧不可用"),
    ("商店/饰品", ["商店", "饰品", "合成", "观测", "白棉花"], "tasks/mirror/in_shop.py；策略受队伍配置和饰品模板影响，不能仅按标题更改购买/合成偏好"),
    ("事件", ["事件", "选项", "判定"], "tasks/event_page.py、battle.py；事件恢复回归通过，具体事件帧未提供则不认定同根因"),
    ("模拟器/显示环境", ["模拟器", "mumu", "MUMU", "锁屏", "分辨率", "萤幕", "屏幕", "盖子"], "module/automation及game_and_screen；需对应Windows/MuMu/显示环境，未改驱动或下载模拟器"),
    ("启动/退出/定时", ["启动", "关闭", "打不开", "退出", "定时", "崩溃", "报错"], "script_task_scheme.py、game.py；失败退出哨兵与启动有界保护测试通过，原生崩溃仍需dump"),
    ("日常/换体", ["日常", "纽本", "钮本", "纺锤", "体力", "换饼", "经验"], "tasks/daily/luxcavation.py及base；日常恢复/编队/事件测试通过，游戏进度和消费路径未实机执行"),
]
rows = ["# 上游开放 Issue 适用性核对", "", "范围：209条开放报告按正文症状与当前模块聚类核对；不是209项实机复现或全附件审计。分类完成，证据不足是审核结论而非证明不存在。混合功能请求不自动排除其缺陷描述。", "", "| Issue | 标题 | 状态 | 依据/边界 |", "|---|---|---|---|"]
for i in issues:
    body = i.get("body") or ""
    status, reason = verified.get(i["number"], ("证据不足／未完成深入验证", "旧报告不能证明当前分支仍存在；未复现对应配置、截图和附件"))
    if i["number"] not in verified:
        status = "环境或证据不足"
        reason = "报告信息不足以建立当前版本可重复用例；不改配置或猜测识别阈值"
        for group, keywords, evidence in groups:
            if any(word in i["title"] for word in keywords):
                reason = group + "：" + evidence
                break
    if i["number"] not in verified and ("描述你想要的新功能" in body or "[feature]" in i["title"].lower()):
        status, reason = "功能请求初筛", "不扩展需求；混合缺陷描述仍需进一步核验，不视为已排除"
    rows.append(f"| [#{i['number']}]({i['html_url']}) | {i['title'].replace('|', '/')} | {status} | {reason} |")
(root / "issue-matrix.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(f"生成 {len(issues)} 行初筛记录")
