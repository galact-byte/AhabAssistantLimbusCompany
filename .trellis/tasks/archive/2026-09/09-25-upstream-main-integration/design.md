# 上游融合设计

以 `git merge` 保留 `KIYI671` 上游 `main@ddc2204` 的祖先，不使用覆盖式文件同步。预检树 `63f7762` 仅加入特征匹配输入保护并更换季节入口图片；对 `module/automation/automation.py` 用最终合并树与 fork HEAD 比对，确认本地 `checkpoint`、`take_screenshot_with_color`、`_run_full_ocr`、业务截图恢复未被覆盖。

特征匹配的失效模板集合随 `clear_img_cache()` 清理；若资源同步不走该清理路径，须限制缓存行为或添加明确失效机制，避免首次缺资源后永久忽略已同步图片。对空截图与空裁剪维持返回 `None` 的失败语义。优先复用现有 `ImageUtils` 和测试双替身，不增加依赖或修改用户配置。

正常历史合并失败时保留预合并 HEAD；只撤销本次未提交的合并状态，不清理无关未跟踪任务目录。无自动推送和部署。
