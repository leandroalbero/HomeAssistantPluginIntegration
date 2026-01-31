"""Base device parser class."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass
import logging

_LOGGER = logging.getLogger(__name__)


@dataclass
class DeviceAttribute:
    """Device attribute definition."""

    key: str
    name: str
    attr_type: str
    step: int = 1
    value_range: Optional[str] = None
    value_map: Optional[Dict[str, str]] = None
    read_write: str = "RW"


class BaseDeviceParser(ABC):
    """Base class for device parsers."""

    @property
    @abstractmethod
    def device_type(self) -> str:
        """Return device type code."""
        pass

    @property
    @abstractmethod
    def feature_code(self) -> str:
        """Return feature code."""
        pass

    @property
    @abstractmethod
    def attributes(self) -> Dict[str, DeviceAttribute]:
        """Return device attributes."""
        pass

    def remove_attribute(self, key: str) -> None:
        """Remove specified attribute."""
        attributes = self.attributes
        if key in attributes:
            del attributes[key]

    def parse_status(self, status: Dict[str, Any]) -> Dict[str, Any]:
        """Parse device status."""
        _LOGGER.debug(
            "Parsing status for device type %s-%s",
            self.device_type,
            self.feature_code,
        )

        parsed_status = {}
        for key, attr in self.attributes.items():
            if key in status:
                value = status[key]
                try:
                    if attr.value_map and value in attr.value_map:
                        parsed_value = attr.value_map[value]
                    elif attr.attr_type == "Number":
                        parsed_value = float(value)
                    else:
                        parsed_value = value
                    parsed_status[key] = parsed_value
                except (ValueError, TypeError) as err:
                    _LOGGER.warning(
                        "Failed to parse attribute %s (%s) with value %s: %s",
                        key,
                        attr.name,
                        value,
                        err,
                    )
                    continue

        return parsed_status

    def validate_value(self, key: str, value: Any) -> bool:
        """Validate value for a given attribute."""
        if key not in self.attributes:
            _LOGGER.warning("Attribute %s not found", key)
            return False

        attr = self.attributes[key]
        if attr.read_write == "R":
            _LOGGER.warning("Attribute %s is read-only", key)
            return False

        if attr.value_range:
            try:
                # Handle range like "16~32,61~90"
                ranges = attr.value_range.split(",")
                num_value = float(value)

                for r in ranges:
                    if "~" in r:
                        min_val, max_val = map(float, r.split("~"))
                        if min_val <= num_value <= max_val:
                            return True
                    elif num_value == float(r):
                        return True

                _LOGGER.warning(
                    "Value %s is outside valid range %s", value, attr.value_range
                )
                return False
            except (ValueError, TypeError) as err:
                _LOGGER.warning("Failed to validate range: %s", err)
                return False

        if attr.value_map:
            valid = str(value) in attr.value_map.keys()
            if not valid:
                _LOGGER.warning(
                    "Value %s not in valid values: %s",
                    value,
                    list(attr.value_map.keys()),
                )
            return valid

        return True
