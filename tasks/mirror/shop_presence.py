import re
from dataclasses import dataclass
from typing import Literal

MAP_LEGEND_THRESHOLD = 0.75
SHOP_CONTROL_THRESHOLD = 0.8
SHOP_COINS_THRESHOLD = 0.8

_MAP_OCR_RE = re.compile(r"正在探索第.+层")


@dataclass(frozen=True)
class ShopPresence:
    state: Literal["shop", "map", "unknown"]
    reason: str


def _normalized(text: str) -> str:
    return "".join(text.split())


def _has_map_ocr(ocr_texts: list[str]) -> bool:
    return any(_MAP_OCR_RE.search(_normalized(text)) for text in ocr_texts)


def _meets(score: float | None, threshold: float) -> bool:
    return score is not None and score >= threshold


def resolve_mirror_shop_presence(
    ocr_texts: list[str],
    *,
    shop_coins: float | None = None,
    legend: float | None = None,
    leave: float | None = None,
    heal: float | None = None,
    shop_return: float | None = None,
) -> ShopPresence:
    """仅从 OCR 文本和模板分数判定地图、商店或证据不足。"""
    if _has_map_ocr(ocr_texts):
        return ShopPresence(state="map", reason="map_ocr")
    if _meets(legend, MAP_LEGEND_THRESHOLD):
        return ShopPresence(state="map", reason="map_legend")

    shop_control = any(
        _meets(score, SHOP_CONTROL_THRESHOLD) for score in (leave, heal, shop_return)
    )
    if _meets(shop_coins, SHOP_COINS_THRESHOLD) and shop_control:
        return ShopPresence(state="shop", reason="shop_controls")
    return ShopPresence(state="unknown", reason="insufficient_evidence")


SHOP_COINS_ASSET = "mirror/shop/shop_coins_assets.png"
MAP_LEGEND_ASSET = "mirror/road_in_mir/legend_assets.png"
SHOP_LEAVE_ASSET = "mirror/shop/leave_assets.png"
SHOP_HEAL_ASSET = "mirror/shop/heal_sinner/heal_sinner_assets.png"
SHOP_RETURN_ASSET = "mirror/shop/return_assets.png"


def inspect_mirror_shop_presence(auto) -> ShopPresence:
    """从当前截图采集 OCR 与模板分数，再交给纯解析。调用方负责截图。"""
    legend = auto.get_image_match_score(MAP_LEGEND_ASSET)
    if _meets(legend, MAP_LEGEND_THRESHOLD):
        return ShopPresence(state="map", reason="map_legend")
    entries = auto.get_ocr_entries()
    ocr_texts = [text for text, *_rest in entries]
    if _has_map_ocr(ocr_texts):
        return ShopPresence(state="map", reason="map_ocr")
    return resolve_mirror_shop_presence(
        ocr_texts,
        shop_coins=auto.get_image_match_score(SHOP_COINS_ASSET),
        legend=legend,
        leave=auto.get_image_match_score(SHOP_LEAVE_ASSET),
        heal=auto.get_image_match_score(SHOP_HEAL_ASSET),
        shop_return=auto.get_image_match_score(SHOP_RETURN_ASSET),
    )


def resolve_shop_leave_dialog(entries) -> tuple[bool, tuple[int, int] | None]:
    """离店标题授权弹窗状态；同行、标题下方且取消右侧的唯一确认才可点击。"""
    titles = [box for text, box in entries if "要离开商店吗" in _normalized(text)]
    if not titles:
        return False, None
    if len(titles) != 1:
        return True, None
    x1, y1, x2, y2 = titles[0]
    width, height = x2 - x1, y2 - y1
    if width <= 0 or height <= 0:
        return True, None
    cancels = [box for text, box in entries if _normalized(text).lstrip("×xX") == "取消"]
    confirms = [box for text, box in entries if _normalized(text) == "确认"]
    candidates = []
    for box in confirms:
        left, top, right, bottom = box
        cx, cy = (left + right) // 2, (top + bottom) // 2
        if not (right > left and bottom > top and y2 < cy < y2 + height * 6
                and x1 - width / 2 < cx < x2 + width / 2):
            continue
        if any(c[2] < left and abs((c[1] + c[3]) / 2 - cy) <= height
               and c[0] >= x1 - width / 2 for c in cancels):
            candidates.append((cx, cy))
    return True, candidates[0] if len(candidates) == 1 else None


def should_end_shop_leave(presence: ShopPresence) -> bool:
    return presence.state == "map"


def is_on_mirror_map(auto, *, use_ocr: bool = True) -> bool:
    """地图证据（legend>=0.75，可选探索 OCR）。不要用默认 0.8 的 find_element。"""
    get_score = getattr(auto, "get_image_match_score", None)
    legend = get_score(MAP_LEGEND_ASSET) if callable(get_score) else None
    if _meets(legend, MAP_LEGEND_THRESHOLD):
        return True
    if not use_ocr:
        return False
    get_entries = getattr(auto, "get_ocr_entries", None)
    if not callable(get_entries):
        return False
    return _has_map_ocr([text for text, *_rest in get_entries()])
