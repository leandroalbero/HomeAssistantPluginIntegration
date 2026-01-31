"""Parser for Heat Pump (035-699) device type."""

from typing import Dict

from .base import BaseDeviceParser, DeviceAttribute


class HeatPump035699Parser(BaseDeviceParser):
    """Parser for Heat Pump 035-699 device type."""

    @property
    def device_type(self) -> str:
        return "035"

    @property
    def feature_code(self) -> str:
        return "699"

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
                value_range="0,1,2,3,4,5,6,7,8,9,10,11,12",
                value_map={
                    "0": "Off",
                    "1": "Heat",
                    "2": "Cool",
                    "3": "Auto",
                    "4": "Hot Water",
                    "5": "Heat + Hot Water",
                    "6": "Cool + Hot Water",
                    "7": "Auto + Hot Water",
                    "8": "Standard",
                    "9": "Eco",
                    "10": "Dual Hot Water",
                    "11": "Dual 1",
                    "12": "Electric Hot Water",
                },
                read_write="RW",
            ),
            "t_temp": DeviceAttribute(
                key="t_temp",
                name="Target Temperature",
                attr_type="Number",
                step=1,
                value_range="16~32",
                read_write="RW",
            ),
            "f_temp_in": DeviceAttribute(
                key="f_temp_in",
                name="Indoor Temperature",
                attr_type="Number",
                read_write="R",
            ),
            "t_dhw_temp": DeviceAttribute(
                key="t_dhw_temp",
                name="DHW Target Temperature",
                attr_type="Number",
                step=1,
                value_range="30~60",
                read_write="RW",
            ),
            "f_dhw_temp": DeviceAttribute(
                key="f_dhw_temp",
                name="DHW Current Temperature",
                attr_type="Number",
                read_write="R",
            ),
            "t_zone1water_settemp1": DeviceAttribute(
                key="t_zone1water_settemp1",
                name="Zone 1 Target Temperature",
                attr_type="Number",
                step=1,
                value_range="16~32",
                read_write="RW",
            ),
            "f_zone1water_temp1": DeviceAttribute(
                key="f_zone1water_temp1",
                name="Zone 1 Current Temperature",
                attr_type="Number",
                read_write="R",
            ),
            "t_zone2water_settemp2": DeviceAttribute(
                key="t_zone2water_settemp2",
                name="Zone 2 Target Temperature",
                attr_type="Number",
                step=1,
                value_range="16~32",
                read_write="RW",
            ),
            "f_zone2water_temp2": DeviceAttribute(
                key="f_zone2water_temp2",
                name="Zone 2 Current Temperature",
                attr_type="Number",
                read_write="R",
            ),
            "f_in_water_temp": DeviceAttribute(
                key="f_in_water_temp",
                name="Inlet Water Temperature",
                attr_type="Number",
                read_write="R",
            ),
            "f_out_water_temp": DeviceAttribute(
                key="f_out_water_temp",
                name="Outlet Water Temperature",
                attr_type="Number",
                read_write="R",
            ),
            "f_power_consumption": DeviceAttribute(
                key="f_power_consumption",
                name="Power Consumption",
                attr_type="Number",
                read_write="R",
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
