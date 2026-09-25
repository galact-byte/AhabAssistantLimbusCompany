# 上游与失败截图只读核查

- fork `HEAD=0745ff9`，上游 `main=ddc22040d1baf3f86fcd94c5384eda038ab8d439`，共同基点 `41299bb84dace71dbb57395f580ddb05988be7e2`，本地独有 53 个、上游独有 5 个提交。
- `git diff HEAD...upstream/main`：`assets/images/default/share/home/season_assets.png`、`module/automation/automation.py`，后者新增 19 行。`git merge-tree --write-tree HEAD upstream/main` 得到 `63f7762bf8177bdbb371bbd8b1a0a94ddb87cd3a`，无冲突输出。自动合并仅新增该 19 行并替换图像，不删除本地彩色帧/恢复/缓存代码。
- 上游非 merge 提交：`983c413` 特征匹配空输入、`c9894e5` 空裁剪、`2ab8592` 赛季入口图像。
- 两张用户原始截图（03:44、13:49）相同 OCR：列表标题 y=344..371；“剧情关卡” y=377..402；“编队#2” y=422..447。比例 0.625，`header[3]+12*scale < top` 要求首项 top>378.5，实际 377 被排除；降低边界须同时保护标题误入。读图及 `read_team_list` 回放都得到首项 #2、`first_row_at_top=False`。未经实机验证滚轮。
- 09-12 老任务的双父合并提交 `eb4d83d` 和测试证据完整，已用 `--no-commit` 归档；规划时 09-05 与 09-13 仍在等待实机反馈。2026-09-25 用户表示已测试、没有明显问题并要求两项一并归档。归档仅代表关闭原任务，不声称有历史 ONNX dump 的最终根因或覆盖了每项未记录的实机分支。
