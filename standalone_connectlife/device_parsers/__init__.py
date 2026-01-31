"""Device parsers package."""

from typing import Dict, Type
import logging

from .base import BaseDeviceParser
from .base_bean import BaseBeanParser
from .split_ac_009_199 import SplitAC009199Parser
from .window_ac_008_399 import WindowAC008399Parser
from .bean_006_299 import PortableAC006299Parser
from .hum_007 import Dehumidifier007Parser
from .atw_035_699 import HeatPump035699Parser
from .oven_013 import Oven013Parser
from .heatpump_044 import HeatPump044Parser
from .hub_043 import HubController043Parser

_LOGGER = logging.getLogger(__name__)

# Registry of device parsers
DEVICE_PARSERS: Dict[tuple[str, str], Type[BaseDeviceParser]] = {
    ("035", "699"): HeatPump035699Parser,
    ("006", "299"): PortableAC006299Parser,
    ("007", ""): Dehumidifier007Parser,
    ("013", ""): Oven013Parser,
    ("044", ""): HeatPump044Parser,
    ("043", ""): HubController043Parser,
}


def get_device_parser(device_type: str, feature_code: str) -> Type[BaseDeviceParser]:
    """Get device parser for the given device type."""
    _LOGGER.debug("Getting device parser for type %s", device_type)

    # Check for specific parser first (with exact feature code match)
    if (device_type, feature_code) in DEVICE_PARSERS:
        _LOGGER.debug("Found specific parser for %s-%s", device_type, feature_code)
        return DEVICE_PARSERS[(device_type, feature_code)]

    # Check for parser with empty feature code (wildcard match)
    if (device_type, "") in DEVICE_PARSERS:
        _LOGGER.debug("Found parser for %s (generic)", device_type)
        return DEVICE_PARSERS[(device_type, "")]

    # Dehumidifier (007) - any feature code
    if device_type == "007":
        _LOGGER.debug("Using dehumidifier parser for %s", device_type)
        return Dehumidifier007Parser

    # Default bean parser for standard AC types
    supported_device_types = ["009", "008", "006", "016"]
    if device_type in supported_device_types:
        _LOGGER.debug("Using default bean parser for device type %s", device_type)
        return BaseBeanParser

    _LOGGER.warning("Unsupported device type: %s", device_type)
    raise ValueError(f"Unsupported device type: {device_type}")


__all__ = [
    "BaseDeviceParser",
    "BaseBeanParser",
    "SplitAC009199Parser",
    "WindowAC008399Parser",
    "PortableAC006299Parser",
    "Dehumidifier007Parser",
    "HeatPump035699Parser",
    "Oven013Parser",
    "HeatPump044Parser",
    "HubController043Parser",
    "get_device_parser",
    "DEVICE_PARSERS",
]
