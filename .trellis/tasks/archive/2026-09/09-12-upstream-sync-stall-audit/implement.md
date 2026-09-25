## 后续提交与归档核对（2026-09-25）

原实施记录中“未提交”的状态已过期：`eb4d83d` 是双父合并提交，父提交分别为本地 `f221d43` 和上游 `41299bb`，已纳入当前 `main` 历史。变更与测试记录见 `research/integration-review.md`，208 项测试通过、Issue 分类范围和实机未验证边界保持原记录，不将实机项目改写为已验收。本任务按当时的代码融合与排查交付范围归档；新的上游差异由 09-25 任务处理。

- [x] 固定本地与上游提交、保存Issue响应、只读预检冲突。
- [x] 核验原日志与离店无限循环探针，区分推断与事实。
- [x] 用户审阅最终方案后 task.py start；后续主会话直接实施和检查，不派子代理。
- [ ] 读取 before-dev、TDD、change-log；涉及上游UI融合读取两套UI规范，保留现有布局不做重设计。
- [x] 基线 uv run --no-sync pytest；记录依赖不可用，不擅自安装。
- [ ] 为离店连续命中、截图失败、正常返回地图、弹窗优先、恢复失败传播新增RED测试。
- [x] git merge --no-commit --no-ff 41299bb84dace71dbb57395f580ddb05988be7e2；逐一融合5处冲突并审查自动合并文件。
- [x] 最小实现商店有限恢复；回归本地事件选择、失败不退出、彩色检测、地图门闩与新上游监视器生命周期。
- [x] 审核209条开放Issue并记录逐项/聚类适用性；对本地证实的缺陷补RED再修复，环境不足保留未验证标记。
- [x] 全量 uv run --no-sync pytest；uv run --no-sync ruff check 受影响Python文件（区分既有问题）；python -m compileall -q app module tasks utils；git diff --check。
- [x] 全范围审查路径规划、队伍编号和名称、资源归属、恢复边界、退出生命周期。无法运行的实机路径明确列出。
- [ ] 更新CHANGES.md与规范知识；核对gitignore，原始日志不提交；汇总提交分组审批，不推送。

## 最终本地检查（待提交审批）
- 208 passed（9.23秒）；聚焦Ruff、compileall、diff --check通过，无未解决合并冲突。
- 补修主题包截图失败/识别异常绕过预算及失败楼层进度传播，3项RED→GREEN回归。
- 209条开放Issue按正文与模块聚类分类完成，证据不足不等于无缺陷；不包含全附件实机复现。最终范围见research/integration-review.md。
- 提交建议：一个merge提交保留上游历史及集成修复、测试和文档。原始日志已忽略，09-05任务不纳入。按design约定提交需单独审批，当前未提交、不归档。

## 当前验证记录（此前阶段）
- 用户已批准并激活；主会话直接处理。5个冲突已解决并标记，未创建合并提交。
- 基线170 passed；当前205 passed（14.59秒）。商店预算、恢复传播和10–12人数补漏均有先失败再通过的测试；正常回地图/监控/权重为补充兼容性验证。
- 聚焦Ruff、compileall、diff --check通过。全受影响文件Ruff为312项；HEAD基线304、上游312，对比双方诊断并集无新增，详见research/lint-baseline.json。
- research/issue-matrix.md记录209条初筛，未完成全部附件深入审核。#711/#438证实离店预算缺陷；#900/#904相关人数漏判已修，但报告实机根因未定。
- CHANGES.md及商店恢复spec已更新。仍需完成集成审查边界记录、原始证据排除和提交审批；不将未勾项宣称完成。

## 证据与风险点
research/log-audit.md、research/evidence/ 原样日志、research/merge-preview.txt、research/upstream-issues.json、research/upstream-open-issues.json。
禁止以合并无冲突或单个测试成功代替集成验收；不能把所有旧Issue宣称在本机复现。最终提交之前保持可回滚边界，用户原有09-05任务目录不动。
