"""Parser for Dehumidifier (007) device type."""

from typing import Dict

from .base import BaseDeviceParser, DeviceAttribute


class Dehumidifier007Parser(BaseDeviceParser):
    """Parser for Dehumidifier 007 device type."""

    @property
    def device_type(self) -> str:
        return "007"

    @property
    def feature_code(self) -> str:
        return ""

    @property
    def attributes(self) -> Dict[str, DeviceAttribute]:
        return {
            "t_power": DeviceAttribute(
                key="t_power",
                name="Power",
                attr_type="Enum",
                step=1,
                value_range="0,1",
                value_map={"0": "Off", "1": "On"},
                read_write="RW",
            ),
            "t_work_mode": DeviceAttribute(
                key="t_work_mode",
                name="Mode",
                attr_type="Enum",
                step=1,
                value_range="0,1,2,3",
                value_map={
                    "0": "Manual",
                    "1": "Continuous",
                    "2": "Auto",
                    "3": "Dry Clothes",
                },
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
            "t_fan_speed": DeviceAttribute(
                key="t_fan_speed",
                name="Fan Speed",
                attr_type="Enum",
                step=1,
                value_range="0,1,2,3",
                value_map={"0": "Auto", "1": "High", "2": "Medium", "3": "Low"},
                read_write="RW",
            ),
            "f_power_consumption": DeviceAttribute(
                key="f_power_consumption",
                name="Power Consumption",
                attr_type="Number",
                read_write="R",
            ),
            "t_child_lock": DeviceAttribute(
                key="t_child_lock",
                name="Child Lock",
                attr_type="Enum",
                step=1,
                value_range="0,1",
                value_map={"0": "Off", "1": "On"},
                read_write="RW",
            ),
            "f_water_full": DeviceAttribute(
                key="f_water_full",
                name="Water Tank Full",
                attr_type="Enum",
                step=1,
                value_range="0,1",
                value_map={"0": "No", "1": "Yes"},
                read_write="R",
            ),
        }
