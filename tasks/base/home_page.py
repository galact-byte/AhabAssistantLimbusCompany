def find_home_drive(entries: list[tuple[str, tuple[int, int, int, int]]]) -> tuple[int, int] | None:
    """仅以同一导航栏的玻璃窗和驾驶席授权主页导航，避免剧情文字误点。"""
    normalized = [("".join(text.split()), bounds) for text, bounds in entries]
    for text, drive in normalized:
        if text != "驾驶席" or drive[0] >= drive[2] or drive[1] >= drive[3]:
            continue
        for label, window in normalized:
            if label != "玻璃窗" or window[0] >= window[2] or window[1] >= window[3]:
                continue
            if window[2] < drive[0] and max(window[1], drive[1]) < min(window[3], drive[3]):
                return ((drive[0] + drive[2]) // 2, (drive[1] + drive[3]) // 2)
    return None
