"""Parser for Heat Pump/ATW devices (044 series)."""

from typing import Dict

from .base import BaseDeviceParser, DeviceAttribute


class HeatPump044Parser(BaseDeviceParser):
    """Parser for Heat Pump/ATW (Air-to-Water) device type 044.

    Supports heat pump systems with:
    - Multiple heating zones
    - DHW (Domestic Hot Water)
    - Swimming pool heating
    - Various temperature sensors
    - Power monitoring
    - Anti-frost protection
    """

    @property
    def device_type(self) -> str:
        return "044"

    @property
    def feature_code(self) -> str:
        return ""

    @property
    def attributes(self) -> Dict[str, DeviceAttribute]:
        if not hasattr(self, "_attributes"):
            self._attributes = {
                # System Status
                "mode": DeviceAttribute(
                    key="mode",
                    name="Operating Mode",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2,3",
                    value_map={"0": "Off", "1": "Heating", "2": "Cooling", "3": "Auto"},
                    read_write="RW",
                ),
                "realRunMode": DeviceAttribute(
                    key="realRunMode",
                    name="Current Run Mode",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2,3,4,5",
                    value_map={
                        "0": "Standby",
                        "1": "Heating",
                        "2": "Cooling",
                        "3": "DHW",
                        "4": "Defrost",
                        "5": "Emergency",
                    },
                    read_write="R",
                ),
                # Zone 1 (Heating Circuit 1)
                "c1_SW_ON": DeviceAttribute(
                    key="c1_SW_ON",
                    name="Zone 1 Power",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "c1R1T": DeviceAttribute(
                    key="c1R1T",
                    name="Zone 1 Room Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "c1R2T": DeviceAttribute(
                    key="c1R2T",
                    name="Zone 1 Room Temperature 2",
                    attr_type="Number",
                    read_write="R",
                ),
                "c1R3T": DeviceAttribute(
                    key="c1R3T",
                    name="Zone 1 Room Temperature 3",
                    attr_type="Number",
                    read_write="R",
                ),
                "c1R4T": DeviceAttribute(
                    key="c1R4T",
                    name="Zone 1 Room Temperature 4",
                    attr_type="Number",
                    read_write="R",
                ),
                "Trc1R1": DeviceAttribute(
                    key="Trc1R1",
                    name="Zone 1 Target Temperature",
                    attr_type="Number",
                    step=1,
                    value_range="16~30",
                    read_write="RW",
                ),
                "Trc1R2": DeviceAttribute(
                    key="Trc1R2",
                    name="Zone 1 Target Temperature 2",
                    attr_type="Number",
                    step=1,
                    value_range="16~30",
                    read_write="RW",
                ),
                "Trc1R3": DeviceAttribute(
                    key="Trc1R3",
                    name="Zone 1 Target Temperature 3",
                    attr_type="Number",
                    step=1,
                    value_range="16~30",
                    read_write="RW",
                ),
                "Trc1R4": DeviceAttribute(
                    key="Trc1R4",
                    name="Zone 1 Target Temperature 4",
                    attr_type="Number",
                    step=1,
                    value_range="16~30",
                    read_write="RW",
                ),
                "c1R1_SW": DeviceAttribute(
                    key="c1R1_SW",
                    name="Zone 1 Room 1 Active",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "c1R2_SW": DeviceAttribute(
                    key="c1R2_SW",
                    name="Zone 1 Room 2 Active",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "c1ws": DeviceAttribute(
                    key="c1ws",
                    name="Zone 1 Water Supply Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                # Zone 2 (Heating Circuit 2)
                "c2_SW_ON": DeviceAttribute(
                    key="c2_SW_ON",
                    name="Zone 2 Power",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "c2R1T": DeviceAttribute(
                    key="c2R1T",
                    name="Zone 2 Room Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "c2R2T": DeviceAttribute(
                    key="c2R2T",
                    name="Zone 2 Room Temperature 2",
                    attr_type="Number",
                    read_write="R",
                ),
                "c2R3T": DeviceAttribute(
                    key="c2R3T",
                    name="Zone 2 Room Temperature 3",
                    attr_type="Number",
                    read_write="R",
                ),
                "c2R4T": DeviceAttribute(
                    key="c2R4T",
                    name="Zone 2 Room Temperature 4",
                    attr_type="Number",
                    read_write="R",
                ),
                "Trc2R1": DeviceAttribute(
                    key="Trc2R1",
                    name="Zone 2 Target Temperature",
                    attr_type="Number",
                    step=1,
                    value_range="16~30",
                    read_write="RW",
                ),
                "c2ws": DeviceAttribute(
                    key="c2ws",
                    name="Zone 2 Water Supply Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                # DHW (Domestic Hot Water)
                "DHW_SW_ON": DeviceAttribute(
                    key="DHW_SW_ON",
                    name="DHW Power",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "DHWs": DeviceAttribute(
                    key="DHWs",
                    name="DHW Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2",
                    value_map={"0": "Off", "1": "Heating", "2": "Ready"},
                    read_write="R",
                ),
                "TDHW": DeviceAttribute(
                    key="TDHW",
                    name="DHW Target Temperature",
                    attr_type="Number",
                    step=1,
                    value_range="30~60",
                    read_write="RW",
                ),
                "TDHWS": DeviceAttribute(
                    key="TDHWS",
                    name="DHW Current Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "Ttos": DeviceAttribute(
                    key="Ttos",
                    name="DHW Tank Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "Defrost_DHW_s": DeviceAttribute(
                    key="Defrost_DHW_s",
                    name="DHW Defrost Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                "DHW_Boost_s": DeviceAttribute(
                    key="DHW_Boost_s",
                    name="DHW Boost Active",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                # Swimming Pool
                "SWP_SW_ON": DeviceAttribute(
                    key="SWP_SW_ON",
                    name="Pool Heating Power",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "SWPs": DeviceAttribute(
                    key="SWPs",
                    name="Pool Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "Heating"},
                    read_write="R",
                ),
                "Tswp": DeviceAttribute(
                    key="Tswp",
                    name="Pool Current Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "Tswps": DeviceAttribute(
                    key="Tswps",
                    name="Pool Target Temperature",
                    attr_type="Number",
                    step=1,
                    value_range="20~35",
                    read_write="RW",
                ),
                "Capacity_SWP": DeviceAttribute(
                    key="Capacity_SWP",
                    name="Pool Heating Capacity",
                    attr_type="Number",
                    read_write="R",
                ),
                # Air-to-Water
                "A2W_SW_ON": DeviceAttribute(
                    key="A2W_SW_ON",
                    name="A2W System Power",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                # Temperature Sensors
                "Ta_2": DeviceAttribute(
                    key="Ta_2",
                    name="Outdoor Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "Ta_24": DeviceAttribute(
                    key="Ta_24",
                    name="Outdoor Temperature 24h Avg",
                    attr_type="Number",
                    read_write="R",
                ),
                "Ta_ao": DeviceAttribute(
                    key="Ta_ao",
                    name="Outdoor Air Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "Trl": DeviceAttribute(
                    key="Trl",
                    name="Return Line Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "Trg": DeviceAttribute(
                    key="Trg",
                    name="Supply Line Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "Twi": DeviceAttribute(
                    key="Twi",
                    name="Water Inlet Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "Two": DeviceAttribute(
                    key="Two",
                    name="Water Outlet Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "Two2": DeviceAttribute(
                    key="Two2",
                    name="Water Outlet Temperature 2",
                    attr_type="Number",
                    read_write="R",
                ),
                "Ts_c1_water": DeviceAttribute(
                    key="Ts_c1_water",
                    name="Zone 1 Water Sensor Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "Ts_c2_water": DeviceAttribute(
                    key="Ts_c2_water",
                    name="Zone 2 Water Sensor Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                # Power and Capacity
                "Pw": DeviceAttribute(
                    key="Pw",
                    name="Current Power Consumption (W)",
                    attr_type="Number",
                    read_write="R",
                ),
                "Capacity_heating": DeviceAttribute(
                    key="Capacity_heating",
                    name="Heating Capacity",
                    attr_type="Number",
                    read_write="R",
                ),
                "Capacity_cooling": DeviceAttribute(
                    key="Capacity_cooling",
                    name="Cooling Capacity",
                    attr_type="Number",
                    read_write="R",
                ),
                "Capacity_DHW": DeviceAttribute(
                    key="Capacity_DHW",
                    name="DHW Heating Capacity",
                    attr_type="Number",
                    read_write="R",
                ),
                "EH1_Power": DeviceAttribute(
                    key="EH1_Power",
                    name="Electric Heater 1 Power (kW)",
                    attr_type="Number",
                    read_write="R",
                ),
                "EH2_Power": DeviceAttribute(
                    key="EH2_Power",
                    name="Electric Heater 2 Power (kW)",
                    attr_type="Number",
                    read_write="R",
                ),
                # Special Modes
                "isSilentMode": DeviceAttribute(
                    key="isSilentMode",
                    name="Silent Mode",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "isECO": DeviceAttribute(
                    key="isECO",
                    name="Eco Mode",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "isNightMode": DeviceAttribute(
                    key="isNightMode",
                    name="Night Mode",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="R",
                ),
                "isFastHotWater": DeviceAttribute(
                    key="isFastHotWater",
                    name="Fast Hot Water",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "isDisinfect": DeviceAttribute(
                    key="isDisinfect",
                    name="Disinfection Mode",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                # Anti-Frost Protection
                "1_Antifrozen_WP1_s": DeviceAttribute(
                    key="1_Antifrozen_WP1_s",
                    name="Anti-Frost Level 1",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                "2_Antifrozen_WP1_s": DeviceAttribute(
                    key="2_Antifrozen_WP1_s",
                    name="Anti-Frost Level 2",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                "Antifrozen_EH1_s": DeviceAttribute(
                    key="Antifrozen_EH1_s",
                    name="Electric Heater Anti-Frost",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                "Antifrozen_HP_s": DeviceAttribute(
                    key="Antifrozen_HP_s",
                    name="Heat Pump Anti-Frost",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                "Defrost_Spaceheat_s": DeviceAttribute(
                    key="Defrost_Spaceheat_s",
                    name="Space Heating Defrost",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                "Anti_Legionella_s": DeviceAttribute(
                    key="Anti_Legionella_s",
                    name="Anti-Legionella Protection",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                # Alarms
                "alarmCode": DeviceAttribute(
                    key="alarmCode",
                    name="System Alarm Code",
                    attr_type="Number",
                    read_write="R",
                ),
                "oilReturn": DeviceAttribute(
                    key="oilReturn",
                    name="Oil Return Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Normal", "1": "Returning"},
                    read_write="R",
                ),
                "isJumpMediumWind": DeviceAttribute(
                    key="isJumpMediumWind",
                    name="Medium Wind Active",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                "isJumpHighWind": DeviceAttribute(
                    key="isJumpHighWind",
                    name="High Wind Active",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                "isRefrigerationJump": DeviceAttribute(
                    key="isRefrigerationJump",
                    name="Refrigeration Jump Active",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                # Hob (if connected)
                "Hob_status": DeviceAttribute(
                    key="Hob_status",
                    name="Hob Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "Hob_zone_1_status": DeviceAttribute(
                    key="Hob_zone_1_status",
                    name="Hob Zone 1 Status",
                    attr_type="Number",
                    read_write="R",
                ),
                "Hob_zone_2_status": DeviceAttribute(
                    key="Hob_zone_2_status",
                    name="Hob Zone 2 Status",
                    attr_type="Number",
                    read_write="R",
                ),
                "Hob_zone_3_status": DeviceAttribute(
                    key="Hob_zone_3_status",
                    name="Hob Zone 3 Status",
                    attr_type="Number",
                    read_write="R",
                ),
                "Hob_zone_4_status": DeviceAttribute(
                    key="Hob_zone_4_status",
                    name="Hob Zone 4 Status",
                    attr_type="Number",
                    read_write="R",
                ),
                "Hob_zone_5_status": DeviceAttribute(
                    key="Hob_zone_5_status",
                    name="Hob Zone 5 Status",
                    attr_type="Number",
                    read_write="R",
                ),
                "HOB_warming_zone_status": DeviceAttribute(
                    key="HOB_warming_zone_status",
                    name="Hob Warming Zone Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="R",
                ),
                "HOB_warming_zone_power_level": DeviceAttribute(
                    key="HOB_warming_zone_power_level",
                    name="Hob Warming Zone Power Level",
                    attr_type="Number",
                    step=1,
                    value_range="0~9",
                    read_write="RW",
                ),
                # Solar
                "Tsolar": DeviceAttribute(
                    key="Tsolar",
                    name="Solar Collector Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
            }
        return self._attributes

    @attributes.setter
    def attributes(self, value: Dict[str, DeviceAttribute]):
        self._attributes = value
