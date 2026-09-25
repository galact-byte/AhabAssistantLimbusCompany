# 上游自动化输入保护：RED

命令：`.venv/Scripts/python.exe -m pytest tests/test_feature_matching_input_guards.py -q`

结果：`4 failed in 1.97s`。旧版 `find_feature_element` 在模板 None、截图 None、空裁剪时均将无效数据交给特征匹配：测试引擎替身返回 `(12, 20)`，结果违背预期的 `None`。旧版 `clear_img_cache` 清空普通缓存，却不清除缺模板标记。四项均针对实际行为失败，非导入或语法错误。原始输出保留在本轮命令记录。
