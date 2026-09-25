# v1.5.9 发布核验

用户明确批准提交、推送和发布后，主会话执行，无子代理。

- 提交：f72ae7b7d5edf84c4fbea4cb89dcbea363beb126；origin/main与v1.5.9解引用均指向该提交。
- GitHub Actions：34750999311；build / build及release均success。
- Release：https://github.com/galact-byte/AhabAssistantLimbusCompany/releases/tag/v1.5.9
- 发布：2026-09-13T10:10:06Z；非草稿、非预发布，latest=v1.5.9。
- 回读正文与release-notes/v1.5.9.md规范化换行后逐字一致。
- 资产：AALC_v1.5.9.7z，160066877字节，state=uploaded。
- GitHub资产SHA256：57059ef2e2b9a63f44ac7d11164ff23c96e3c2dc8df3b835aea3623817de4f70。
- 发布前全量测试259 passed in 10.26s；真实Qt/ONNX六轮探针退出0；compileall和git diff --check通过。

原始远端元数据：release-remote.json；测试：release-tests.txt及release-native-probe.txt。

仅提交32个本次源码、测试、spec、CHANGES及发布说明文件；没有上传旧任务目录、原日志、系统事件或用户配置。工作区剩余三个未跟踪任务目录保持原样。本机G盘未部署，未执行真实游戏/无人值守长测；历史dump未决，任务保持in_progress供后续验收。不主动触发独立MirrorChyan分发流程。
