"""Base bean parser for most AC devices."""

from typing import Dict

from .base import BaseDeviceParser, DeviceAttribute


class BaseBeanParser(BaseDeviceParser):
    """Parser for standard bean-style devices (009, 008, 006)."""

    @property
    def device_type(self) -> str:
        return "1"

    @property
    def feature_code(self) -> str:
        return "2"

    def remove_attribute(self, key: str) -> None:
        """Remove specified attribute."""
        # Ensure attributes are initialized first
        attrs = self.attributes
        if key in attrs:
            del attrs[key]

    @property
    def attributes(self) -> Dict[str, DeviceAttribute]:
        if not hasattr(self, "_attributes"):
            self._attributes = {
                "t_work_mode": DeviceAttribute(
                    key="t_work_mode",
                    name="Mode",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2,3,4,5",
                    value_map={
                        "0": "Fan",
                        "1": "Heat",
                        "2": "Cool",
                        "3": "Dry",
                        "4": "Auto",
                        "5": "E-star",
                    },
                    read_write="RW",
                ),
                "t_power": DeviceAttribute(
                    key="t_power",
                    name="Power",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "t_temp": DeviceAttribute(
                    key="t_temp",
                    name="Target Temperature",
                    attr_type="Number",
                    step=1,
                    value_range="16~32,61~90",
                    read_write="RW",
                ),
                "t_fan_speed": DeviceAttribute(
                    key="t_fan_speed",
                    name="Fan Speed",
                    attr_type="Enum",
                    step=1,
                    value_range="0,5,6,7,8,9",
                    value_map={
                        "2": "Low",
                        "3": "Medium",
                        "4": "High",
                        "0": "Auto",
                        "5": "Low",
                        "6": "Mid-Low",
                        "7": "Mid",
                        "8": "Mid-High",
                        "9": "High",
                    },
                    read_write="RW",
                ),
                "t_up_down": DeviceAttribute(
                    key="t_up_down",
                    name="Swing Vertical",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "t_temp_type": DeviceAttribute(
                    key="t_temp_type",
                    name="Temperature Unit",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Celsius", "1": "Fahrenheit"},
                    read_write="RW",
                ),
                "t_left_right": DeviceAttribute(
                    key="t_left_right",
                    name="Swing Horizontal",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "f_power_consumption": DeviceAttribute(
                    key="f_power_consumption",
                    name="Power Consumption",
                    attr_type="Number",
                    read_write="R",
                ),
                "t_fan_mute": DeviceAttribute(
                    key="t_fan_mute",
                    name="Quiet Mode",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "f_temp_in": DeviceAttribute(
                    key="f_temp_in",
                    name="Indoor Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "t_8heat": DeviceAttribute(
                    key="t_8heat",
                    name="8°C Heat",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "t_eco": DeviceAttribute(
                    key="t_eco",
                    name="Eco Mode",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "t_humidity": DeviceAttribute(
                    key="t_humidity",
                    name="Target Humidity",
                    attr_type="Number",
                    step=5,
                    value_range="30~80",
                    read_write="RW",
                ),
                "f_humidity": DeviceAttribute(
                    key="f_humidity",
                    name="Indoor Humidity",
                    attr_type="Number",
                    step=1,
                    value_range="30~90",
                    read_write="R",
                ),
                "t_super": DeviceAttribute(
                    key="t_super",
                    name="Turbo",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
            }
        return self._attributes

    @attributes.setter
    def attributes(self, value: Dict[str, DeviceAttribute]):
        self._attributes = value
