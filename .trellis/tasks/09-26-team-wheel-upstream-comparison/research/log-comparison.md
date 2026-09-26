# 2026-09-26 日志与原始截图对照

- 本地原始日志：`G:/BaiduNetdiskDownload/AALC_v1.5.11/AALC/logs/debugLog.log`（166 行）。04:04:15 开始寻找队伍；04:04:18/20/23/26 OCR 都显示“剧情关卡、编队#2..#7”，04:04:26 报“无法确认编队滚轮生效”，随后日常任务提前失败，04:04:26.516 UI 收尾；12:20 两条窗口位置日志。此处是自动任务已停而游戏在编队界面，不是工作线程持续阻塞。
- 本地原始截图：`G:/BaiduNetdiskDownload/AALC_v1.5.11/AALC/logs/team-selection-failed-20260926-040426-352315.png`；画面为 1600x900，顶端标题“编队#2”、左侧首行“剧情关卡”、其后 #2..#7。
- 离线验证命令：`.venv/Scripts/python.exe -c "import numpy as np; from module.ocr import ocr; from tasks.team_list import read_team_list; p='G:/BaiduNetdiskDownload/AALC_v1.5.11/AALC/logs/team-selection-failed-20260926-040426-352315.png'; r=ocr.run(p); e=[(t,(int(np.min(b[:,0])),int(np.min(b[:,1])),int(np.max(b[:,0])),int(np.max(b[:,1])))) for t,b in zip(r.txts,r.boxes)]; page=read_team_list(e,(1500,222),.625); print(page); print(page.first_row_at_top)"`；输出首行中心 (164.5,389.5)，次行 (164,434.5)，`first_row_at_top=True`。Git Bash 输出中文字节发生转码，但 OCR 返回的原始几何及解析通过。
- 上游原始日志：`G:/BaiduNetdiskDownload/AALC_V1.6.0/AALC/logs/debugLog.log.1:20437-20452`，12:21 选日常队 1 后进入战斗；`debugLog.log:8521-8544`，13:24 选镜牢队 2 后确认。上游执行的是旧拖动及坐标点选，不具有本地版本新增的身份核验；两版比较证明本地新路径引入了此中断点，不证明旧版从不选错。
- 候选机制：`tasks/teams/team_formation.py:_reset_team_list` 总是强制下滚探针；`module/automation/input_handlers/input.py:BackgroundInput.mouse_swipe_for_team_scroll` 发 `WM_MOUSEWHEEL` 返回 True 只表明系统调用执行，不表明 Unity 列表消费。具体是 Unity 对消息不响应、目标控件不消费还是光标焦点问题，日志不足以区分，实机需验证。
- 既有任务 `09-20-mirror-team-selection-verification` 已指出 Windows 专用滚轮未实机验证；`09-25-team-list-top-boundary` 只修 OCR 首行门限，本次图像首行已正确入列。
