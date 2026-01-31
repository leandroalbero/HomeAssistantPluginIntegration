"""Parser for Window AC (008-399) device type."""

from typing import Dict

from .base_bean import BaseBeanParser


class WindowAC008399Parser(BaseBeanParser):
    """Parser for Window AC 008-399 device type."""

    @property
    def device_type(self) -> str:
        return "008"

    @property
    def feature_code(self) -> str:
        return "399"
