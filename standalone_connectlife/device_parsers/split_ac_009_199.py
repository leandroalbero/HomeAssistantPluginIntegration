"""Parser for Split AC (009-199) device type."""

from typing import Dict

from .base import BaseDeviceParser, DeviceAttribute


class SplitAC009199Parser(BaseDeviceParser):
    """Parser for Split AC 009-199 device type."""

    @property
    def device_type(self) -> str:
        return "009"

    @property
    def feature_code(self) -> str:
        return "199"

    @property
    def attributes(self) -> Dict[str, DeviceAttribute]:
        return {
            "t_work_mode": DeviceAttribute(
                key="t_work_mode",
                name="Mode",
                attr_type="Enum",
                step=1,
                value_range="0,1,2,3,4",
                value_map={
                    "0": "Fan",
                    "1": "Heat",
                    "2": "Cool",
                    "3": "Dry",
                    "4": "Auto",
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
                    "0": "Auto",
                    "5": "Ultra Low",
                    "6": "Low",
                    "7": "Medium",
                    "8": "High",
                    "9": "Ultra High",
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
            "t_super": DeviceAttribute(
                key="t_super",
                name="Turbo",
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
        }
