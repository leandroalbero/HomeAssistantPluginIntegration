"""Parser for Portable AC (006-299) device type."""

from typing import Dict

from .base_bean import BaseBeanParser


class PortableAC006299Parser(BaseBeanParser):
    """Parser for Portable AC 006-299 device type."""

    @property
    def device_type(self) -> str:
        return "006"

    @property
    def feature_code(self) -> str:
        return "299"
