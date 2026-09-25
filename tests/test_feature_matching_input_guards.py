from types import SimpleNamespace

import numpy as np
import pytest
from PIL import Image

from module.automation import automation as automation_module
from utils.image_utils import ImageUtils


@pytest.mark.parametrize("invalid", ["template", "screenshot", "crop"])
def test_feature_matching_skips_unusable_inputs(monkeypatch, invalid):
    auto = object.__new__(automation_module.Automation)
    auto.screenshot = None if invalid == "screenshot" else Image.fromarray(np.ones((24, 24), dtype=np.uint8))
    monkeypatch.setattr(automation_module, "cfg", SimpleNamespace(set_win_size=1440))
    template = None if invalid == "template" else np.ones((4, 4), dtype=np.uint8)
    monkeypatch.setattr(ImageUtils, "load_image", lambda *args, **kwargs: template)
    monkeypatch.setattr(ImageUtils, "feature_matching", lambda *args: ((12, 20), 10))
    if invalid == "crop":
        monkeypatch.setattr(ImageUtils, "crop", lambda *args: np.empty((0, 0), dtype=np.uint8))

    result = auto.find_feature_element("missing.png", pic_crop=(0, 0, 5, 5) if invalid == "crop" else None)

    assert result is None


def test_missing_template_becomes_matchable_after_cache_refresh(monkeypatch):
    auto = object.__new__(automation_module.Automation)
    auto.img_cache = {}
    auto._unavailable_feature_templates = set()
    auto.screenshot = Image.fromarray(np.ones((24, 24), dtype=np.uint8))
    monkeypatch.setattr(automation_module, "cfg", SimpleNamespace(set_win_size=1440))
    available = [False]
    monkeypatch.setattr(
        ImageUtils,
        "load_image",
        lambda *args, **kwargs: np.ones((4, 4), dtype=np.uint8) if available[0] else None,
    )
    monkeypatch.setattr(ImageUtils, "feature_matching", lambda *args: ((12, 20), 10))

    assert auto.find_feature_element("missing.png") is None
    available[0] = True
    assert auto.find_feature_element("missing.png") is None

    auto.clear_img_cache()

    assert auto.find_feature_element("missing.png") == (12, 20)


def test_clearing_image_cache_retries_previously_missing_template():
    auto = object.__new__(automation_module.Automation)
    auto.img_cache = {"old": "image"}
    auto._unavailable_feature_templates = {"missing.png"}

    auto.clear_img_cache()

    assert not auto.img_cache
    assert not auto._unavailable_feature_templates
