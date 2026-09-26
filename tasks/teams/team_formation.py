from datetime import datetime
from pathlib import Path
from time import sleep

from module.automation import auto
from module.config import cfg
from module.decorator.decorator import begin_and_finish_time_log
from module.logger import log
from tasks.team_list import extend_team_order, matches_team_number, read_team_list, selected_team_matches

NAMED_TEAM_PAGE_SWIPE_DISTANCE = 385
ORDERED_TEAM_COUNT = 40


# 清队
def clean_team():
    scale = cfg.set_win_size / 1440
    while True:
        # 自动截图
        if auto.take_screenshot() is None:
            continue
        if auto.click_element("teams/clear_selection_confirm_assets.png"):
            break
        if (identify_position := auto.find_element("teams/identify_assets.png")) and auto.mouse_action_with_pos(
            [identify_position[0], identify_position[1] + 600 * scale]
        ):
            sleep(0.5)
            auto.take_screenshot()
            if auto.find_element("teams/clear_selection_confirm_assets.png") is None:
                break


@begin_and_finish_time_log(task_name="罪人编队")
# 编队
def team_formation(sinner_team):
    scale = cfg.set_win_size / 1440

    clean_team()
    while auto.take_screenshot() is None:
        continue
    if reset_team := auto.find_element("teams/identify_assets.png"):
        first_sinner = [reset_team[0] - 1800 * scale, reset_team[1] + 130 * scale]
    else:
        log.error("无法找到罪人编队的起始位置")
        return
    sleep(0.5)

    for i in range(1, 13):
        if i in sinner_team:
            sinner = sinner_team.index(i)
        else:
            return
        if sinner <= 5:
            auto.mouse_click(first_sinner[0] + 270 * sinner * scale, first_sinner[1])
        else:
            auto.mouse_click(
                first_sinner[0] + 270 * (sinner - 6) * scale,
                first_sinner[1] + 500 * scale,
            )
        sleep(cfg.mouse_action_interval)


def find_named_team_position(num: int, text_positions: dict[str, list[float]]) -> list[float] | bool:
    """从 OCR 结果中查找指定编号的编队名称，并排除预设项。"""
    matches = [position for text, position in text_positions.items() if matches_team_number(text, num)]
    return matches[0] if len(matches) == 1 else False


TEAM_FRAME_ATTEMPTS = 3
TEAM_SCROLL_ATTEMPTS = 100
TEAM_SELECT_ATTEMPTS = 3


def _read_team_frame(scale):
    for _ in range(TEAM_FRAME_ATTEMPTS):
        if auto.take_screenshot() is not None:
            if auto.find_element("home/first_prompt_assets.png", model="clam") and auto.find_element(
                "home/back_assets.png", model="normal"
            ):
                auto.click_element("home/back_assets.png")
                sleep(0.25)
                continue
            identify = auto.find_element("teams/identify_assets.png")
            if identify:
                entries = auto.get_ocr_entries()
                page = read_team_list(entries, identify, scale)
                if page is not None:
                    return page, entries, identify
        sleep(0.25)
    raise ValueError("截图或编队列表识别不可用")


def _scroll_team_list(page, direction, scale):
    # Windows 的 dy 只有方向语义；模拟器继续使用现有专用手势及像素距离。
    distance = (NAMED_TEAM_PAGE_SWIPE_DISTANCE * scale if cfg.simulator else 1)
    row = page.rows[1] if direction > 0 else page.rows[-2]
    if auto.mouse_swipe_for_team_scroll(*row.position, dy=direction * distance, duration=0.3) is False:
        raise ValueError("当前输入方式不支持安全编队滚动")
    sleep(0.35)
    return _read_team_frame(scale)


def _reset_team_list(frame, scale, *, verify_scroll=True):
    stable = 0
    for _ in range(TEAM_SCROLL_ATTEMPTS):
        next_frame = _scroll_team_list(frame[0], 1, scale)
        stable = stable + 1 if next_frame[0].signature == frame[0].signature else 0
        frame = next_frame
        if stable >= 2:
            if not frame[0].has_known_top_anchor:
                raise ValueError("列表停止滚动但未识别到顶部固定首项")
            if verify_scroll:
                # 静止也可能是后台滚轮未生效；用一次下滚和回顶验证输入，
                # 不为证明首行而遍历无关的40个槽。
                top = frame[0].signature
                probe = _scroll_team_list(frame[0], -1, scale)
                if probe[0].signature == top:
                    raise ValueError("无法确认编队滚轮生效")
                frame = _reset_team_list(probe, scale, verify_scroll=False)
                if frame[0].signature != top:
                    raise ValueError("编队滚动回顶结果不一致")
            return frame
    raise ValueError("编队归顶次数耗尽")


def _scan_team_order(frame, scale, num):
    known = frame[0].names
    stable = 0
    for _ in range(TEAM_SCROLL_ATTEMPTS):
        if cfg.select_team_by_order:
            target = known[num - 1] if len(known) >= num else None
        else:
            matches = [name for name in known if matches_team_number(name, num)]
            if len(matches) > 1:
                raise ValueError("编号对应多个编队")
            target = matches[0] if matches else None
        if target is not None:
            return target, frame
        next_frame = _scroll_team_list(frame[0], -1, scale)
        merged = extend_team_order(known, next_frame[0])
        if merged is None or len(merged) > ORDERED_TEAM_COUNT:
            raise ValueError("列表页间顺序不连续或存在重名")
        known = merged
        stable = stable + 1 if next_frame[0].signature == frame[0].signature else 0
        frame = next_frame
        if stable >= 2:
            raise ValueError("列表无进展，未找到目标编队")
    raise ValueError("编队扫描次数耗尽")


def _team_selection_failed(num, reason):
    log.error(f"选队 {num} 未通过校验：{reason}")
    screenshot = getattr(auto, "screenshot", None)
    if screenshot is not None:
        try:
            path = Path("logs") / f"team-selection-failed-{datetime.now():%Y%m%d-%H%M%S-%f}.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            screenshot.save(path)
            log.warning(f"选队失败画面已保存：{path}")
        except (OSError, ValueError) as error:
            log.warning(f"无法保存选队失败画面：{error}")
    return False


@begin_and_finish_time_log(task_name="寻找队伍")
def select_battle_team(num):
    if not isinstance(num, int) or isinstance(num, bool) or not 1 <= num <= ORDERED_TEAM_COUNT:
        return _team_selection_failed(num, "队伍编号不在1–40内")
    scale = cfg.set_win_size / 1440
    try:
        frame = _read_team_frame(scale)
        matches = [] if cfg.select_team_by_order else [
            name for name in frame[0].names if matches_team_number(name, num)
        ]
        if len(matches) > 1:
            raise ValueError("编号对应多个编队")
        if matches:
            target = matches[0]
        elif cfg.select_team_by_order and frame[0].has_known_top_anchor and num <= len(frame[0].rows):
            target = frame[0].names[num - 1]
        else:
            frame = _reset_team_list(frame, scale)
            target, frame = _scan_team_order(frame, scale, num)
        for attempt in range(TEAM_SELECT_ATTEMPTS):
            row = next(row for row in frame[0].rows if row.name == target)
            auto.mouse_click(*row.position)
            sleep(0.5)
            frame = _read_team_frame(scale)
            if selected_team_matches(frame[1], target, frame[2], scale):
                log.info(f"选队 {num} 已核验：{target}")
                return True
            log.warning(f"选队结果不一致，重试 {attempt + 1}/{TEAM_SELECT_ATTEMPTS}")
        return _team_selection_failed(num, "选后标题校验次数耗尽")
    except Exception as error:
        # OCR/输入后端异常也必须阻止确认；协作取消是 BaseException，不会被吞掉。
        return _team_selection_failed(num, f"{type(error).__name__}: {error}")


def deal_with_spills():
    import cv2
    import numpy as np

    from module.ocr import ocr
    from utils.image_utils import ImageUtils

    scale = cfg.set_win_size / 1440
    sinner_nums_bbox = ImageUtils.get_bbox(ImageUtils.load_image("battle/normal_to_battle_assets.png"))
    sinner_nums_bbox = (
        sinner_nums_bbox[0],
        sinner_nums_bbox[1] - 115 * scale,
        sinner_nums_bbox[2],
        sinner_nums_bbox[3] - 115 * scale,
    )
    sc = ImageUtils.crop(np.array(auto.screenshot), sinner_nums_bbox)
    sc = cv2.bitwise_not(sc)
    mask = cv2.inRange(sc, 220, 255)
    mask = cv2.bitwise_not(mask)
    background = np.zeros((300, 300), dtype=np.uint8)
    h, w = mask.shape[:2]
    y_off = (300 - h) // 2
    x_off = (300 - w) // 2
    background[y_off : y_off + h, x_off : x_off + w] = mask
    try:
        result = ocr.run(background)
        ocr_result = [result.txts[i] for i in range(len(result.txts))]
        ocr_result = "".join(ocr_result)
        log.debug(f"对于配队人数OCR得到：{ocr_result}")
        if "/" in ocr_result:
            result = ocr_result.split("/")
            result = [i.strip() for i in result]
            import re

            now = int(re.sub(r"\D", "", result[-2]))
            max = int(re.sub(r"\D", "", result[-1]))
            if now > max:
                all_selected = auto.find_element("teams/selected.png", find_type="image_with_multiple_targets")
                kernel = np.ones((3, 3), np.uint8)
                for selected in all_selected:
                    try:
                        order_bbox = (
                            selected[0] - 40 * scale,
                            selected[1] - 120 * scale,
                            selected[0] + 40 * scale,
                            selected[1] - 30 * scale,
                        )
                        sc2 = ImageUtils.crop(np.array(auto.screenshot), order_bbox)
                        background2 = np.zeros((300, 300), dtype=np.uint8)
                        h, w = sc2.shape[:2]
                        y_off = (300 - h) // 2
                        x_off = (300 - w) // 2
                        background2[y_off : y_off + h, x_off : x_off + w] = sc2
                        result = ocr.run(background2)
                        ocr_result = [result.txts[i] for i in range(len(result.txts))]
                        ocr_result = "".join(ocr_result)
                        if ocr_result == "G":
                            ocr_result = "6"
                        if int(ocr_result) == 1:
                            # 再腐蚀 3 次
                            background2 = cv2.erode(background2, kernel, iterations=3)
                            # 再膨胀 2 次
                            background2 = cv2.dilate(background2, kernel, iterations=2)
                            result = ocr.run(background2)
                            ocr_result = [result.txts[i] for i in range(len(result.txts))]
                            ocr_result = "".join(ocr_result)
                        if int(ocr_result) > max:
                            auto.mouse_click(selected[0], selected[1])
                    except:
                        continue
    except:
        pass


@begin_and_finish_time_log(task_name="检查队伍剩余战斗力")
def check_team():
    # 至少还有5人可以战斗
    sinner_nums = [f"{a}/{b}" for b in range(5, 13) for a in range(5, b + 1)]
    if auto.find_element(sinner_nums, find_type="text"):
        return True
    else:
        return False


@begin_and_finish_time_log(task_name="加载编队码")
def load_team_code_in_game(team_code: str) -> bool:
    """在游戏中加载编队码

    Args:
        team_code: 编队码字符串

    Returns:
        成功返回 True，失败返回 False
    """
    # 验证当前在队伍选择界面
    if not auto.find_element("mirror/road_to_mir/select_team_confirm_assets.png"):
        log.warning("未在队伍选择界面，跳过编队码加载")
        return False

    # 最多重试3次
    max_retries = 3
    for _ in range(1, max_retries + 1):
        # 截图
        while auto.take_screenshot() is None:
            continue

        # 点击队伍代码按钮
        auto.click_element("teams/team_code_assets.png")
        sleep(1)

        # 查找并点击加载编队码按钮
        auto.click_element("teams/load_team_code_button_assets.png", take_screenshot=True)
        sleep(1)

        # 查找根据取消按钮判断输入框是否出现
        if not auto.find_element("teams/team_code_cancel_button_assets.png", take_screenshot=True):
            # 尝试点击取消按钮返回
            auto.mouse_click_blank()
            sleep(1)
            continue

        # 使用 input_text(text) 直接输入编队码
        auto.input_text(team_code)
        sleep(0.5)  # 等待输入完成

        # 点击确认按钮，最多重试 3 次
        for _ in range(3):
            if auto.click_element("teams/team_code_confirm_button_assets.png", take_screenshot=True):
                sleep(1)
            else:
                break

        # 验证返回队伍选择界面
        if auto.find_element("teams/team_code_assets.png", take_screenshot=True):
            return True
        else:
            auto.click_element("teams/team_code_cancel_button_assets.png")
            sleep(1)

    auto.mouse_click(100, 100)  # 点击左上角关闭
    log.warning(f"加载编队码失败，已重试{max_retries}次: {team_code}")
    return False
