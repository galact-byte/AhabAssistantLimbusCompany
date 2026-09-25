"""编队列表的纯 OCR 几何与页间顺序解析，不依赖自动化运行时。"""
import re
import unicodedata
from dataclasses import dataclass


def normalize_team_name(text: str) -> str:
    return "".join(unicodedata.normalize("NFKC", text).split()).casefold()


def matches_team_number(text: str, number: int) -> bool:
    name = normalize_team_name(text)
    return not re.search(r"预设|preset", name) and bool(re.search(rf"#{number}(?!\d)", name))


@dataclass(frozen=True)
class TeamRow:
    name: str
    position: tuple[float, float]


@dataclass(frozen=True)
class TeamListPage:
    rows: tuple[TeamRow, ...]
    header_y: float
    scale: float

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(row.name for row in self.rows)

    @property
    def signature(self):
        # 滚轮一个刻度可能只移动半行；仅比较名称会误判已经到顶。
        return tuple((row.name, round(row.position[1] / self.scale / 3)) for row in self.rows)

    @property
    def first_row_at_top(self) -> bool:
        return 50 <= (self.rows[0].position[1] - self.header_y) / self.scale <= 95


def read_team_list(entries, identify_position, scale) -> TeamListPage | None:
    x = identify_position[0] - 2150 * scale
    expected_header_y = identify_position[1] + 215 * scale
    headers = [bounds for text, bounds in entries
               if normalize_team_name(text) in {"编队", "teams", "team"}
               and abs((bounds[0] + bounds[2]) / 2 - x) < 110 * scale
               and abs((bounds[1] + bounds[3]) / 2 - expected_header_y) < 35 * scale]
    if len(headers) != 1:
        return None
    header = headers[0]
    header_y = (header[1] + header[3]) / 2
    rows = []
    for text, (left, top, right, bottom) in entries:
        cx, cy = (left + right) / 2, (top + bottom) / 2
        if (x - 120 * scale <= left < right <= x + 120 * scale
                and header[3] + 6 * scale < top < bottom < header_y + 615 * scale):
            name = normalize_team_name(text)
            if not name or re.search(r"预设|preset", name):
                return None
            rows.append(TeamRow(name, (cx, cy)))
    rows.sort(key=lambda row: row.position[1])
    if len(rows) < 2 or len({row.name for row in rows}) != len(rows):
        return None
    # 不能把 OCR 漏掉一整行后的第 N 个文本当作第 N 个编队。
    if any(not 52 * scale < b.position[1] - a.position[1] < 94 * scale
           for a, b in zip(rows, rows[1:])):
        return None
    return TeamListPage(tuple(rows), header_y, scale)


def extend_team_order(known: tuple[str, ...], page: TeamListPage) -> tuple[str, ...] | None:
    names = page.names
    overlaps = [size for size in range(1, min(len(known), len(names)) + 1)
                if known[-size:] == names[:size]]
    if len(overlaps) != 1:
        return None
    additions = names[overlaps[0]:]
    if any(name in known for name in additions):
        return None
    return known + additions


def selected_team_matches(entries, expected: str, identify_position, scale) -> bool:
    # 顶部当前编队标题与左侧列表、预设卡片分区，禁止用列表中出现目标名作为选中证据。
    titles = [normalize_team_name(text) for text, (left, top, right, bottom) in entries
              if 0 <= left < right < 1100 * scale and 0 <= top < bottom < 150 * scale]
    return titles.count(expected) == 1
