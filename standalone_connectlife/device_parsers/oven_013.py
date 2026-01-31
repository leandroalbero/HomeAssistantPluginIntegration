"""Parser for Oven devices (013 series)."""

from typing import Dict

from .base import BaseDeviceParser, DeviceAttribute


class Oven013Parser(BaseDeviceParser):
    """Parser for Oven device type 013.

    Supports ovens with various features including:
    - Multiple baking steps
    - Temperature control
    - Timers
    - Steam functions
    - Door lock
    - Interior light
    - Meat probe
    - Various alarms and notifications
    """

    @property
    def device_type(self) -> str:
        return "013"

    @property
    def feature_code(self) -> str:
        return ""

    @property
    def attributes(self) -> Dict[str, DeviceAttribute]:
        if not hasattr(self, "_attributes"):
            self._attributes = {
                # Power and Status
                "Status": DeviceAttribute(
                    key="Status",
                    name="Power",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "Child_lock": DeviceAttribute(
                    key="Child_lock",
                    name="Child Lock",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "Door": DeviceAttribute(
                    key="Door",
                    name="Door Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Closed", "1": "Open"},
                    read_write="R",
                ),
                "Door_lock": DeviceAttribute(
                    key="Door_lock",
                    name="Door Lock",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Unlocked", "1": "Locked"},
                    read_write="RW",
                ),
                # Step 1 (Main baking step)
                "Step_1_status": DeviceAttribute(
                    key="Step_1_status",
                    name="Step 1 Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2,3",
                    value_map={
                        "0": "Inactive",
                        "1": "Active",
                        "2": "Paused",
                        "3": "Finished",
                    },
                    read_write="RW",
                ),
                "Step_1_set_temperature": DeviceAttribute(
                    key="Step_1_set_temperature",
                    name="Step 1 Target Temperature",
                    attr_type="Number",
                    step=1,
                    value_range="30~300",
                    read_write="RW",
                ),
                "Step_1_bake_mode": DeviceAttribute(
                    key="Step_1_bake_mode",
                    name="Step 1 Bake Mode",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2,3,4,5,6,7,8,9,10",
                    value_map={
                        "0": "Conventional",
                        "1": "Fan",
                        "2": "Grill",
                        "3": "Bottom Heat",
                        "4": "Defrost",
                        "5": "Steam",
                        "6": "Microwave",
                        "7": "Combination",
                        "8": "Pizza",
                        "9": "Eco",
                        "10": "Fast Preheat",
                    },
                    read_write="RW",
                ),
                "Step_1_set_heater_system": DeviceAttribute(
                    key="Step_1_set_heater_system",
                    name="Step 1 Heater System",
                    attr_type="Number",
                    step=1,
                    read_write="RW",
                ),
                "Step_1_duration": DeviceAttribute(
                    key="Step_1_duration",
                    name="Step 1 Duration (minutes)",
                    attr_type="Number",
                    step=1,
                    value_range="0~1440",
                    read_write="RW",
                ),
                "Step_1_remaining_time": DeviceAttribute(
                    key="Step_1_remaining_time",
                    name="Step 1 Remaining Time (seconds)",
                    attr_type="Number",
                    read_write="R",
                ),
                # Step 2
                "Step_2_status": DeviceAttribute(
                    key="Step_2_status",
                    name="Step 2 Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2,3",
                    value_map={
                        "0": "Inactive",
                        "1": "Active",
                        "2": "Paused",
                        "3": "Finished",
                    },
                    read_write="RW",
                ),
                "Step_2_set_temperature": DeviceAttribute(
                    key="Step_2_set_temperature",
                    name="Step 2 Target Temperature",
                    attr_type="Number",
                    step=1,
                    value_range="30~300",
                    read_write="RW",
                ),
                # Step 3
                "Step_3_status": DeviceAttribute(
                    key="Step_3_status",
                    name="Step 3 Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2,3",
                    value_map={
                        "0": "Inactive",
                        "1": "Active",
                        "2": "Paused",
                        "3": "Finished",
                    },
                    read_write="RW",
                ),
                "Step_3_set_temperature": DeviceAttribute(
                    key="Step_3_set_temperature",
                    name="Step 3 Target Temperature",
                    attr_type="Number",
                    step=1,
                    value_range="30~300",
                    read_write="RW",
                ),
                # Current baking info
                "Current_baking_step": DeviceAttribute(
                    key="Current_baking_step",
                    name="Current Baking Step",
                    attr_type="Number",
                    read_write="R",
                ),
                "Oven_measured_temperature": DeviceAttribute(
                    key="Oven_measured_temperature",
                    name="Current Oven Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                "Oven_temperature_unit": DeviceAttribute(
                    key="Oven_temperature_unit",
                    name="Temperature Unit",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Celsius", "1": "Fahrenheit"},
                    read_write="RW",
                ),
                # Sand Timers
                "Sand_timer_1_status": DeviceAttribute(
                    key="Sand_timer_1_status",
                    name="Timer 1 Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2,3,4,5,6,7",
                    value_map={
                        "0": "Inactive",
                        "1": "Running",
                        "2": "Paused",
                        "5": "Elapsed",
                        "7": "Finished",
                    },
                    read_write="RW",
                ),
                "Sand_timer_1_duration_minutes": DeviceAttribute(
                    key="Sand_timer_1_duration_minutes",
                    name="Timer 1 Duration (minutes)",
                    attr_type="Number",
                    step=1,
                    value_range="0~255",
                    read_write="RW",
                ),
                "Sand_timer_2_status": DeviceAttribute(
                    key="Sand_timer_2_status",
                    name="Timer 2 Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2,3,4,5,6,7",
                    value_map={
                        "0": "Inactive",
                        "1": "Running",
                        "2": "Paused",
                        "5": "Elapsed",
                        "7": "Finished",
                    },
                    read_write="RW",
                ),
                "Sand_timer_3_status": DeviceAttribute(
                    key="Sand_timer_3_status",
                    name="Timer 3 Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2,3,4,5,6,7",
                    value_map={
                        "0": "Inactive",
                        "1": "Running",
                        "2": "Paused",
                        "5": "Elapsed",
                        "7": "Finished",
                    },
                    read_write="RW",
                ),
                # Steam Functions
                "Steam_123": DeviceAttribute(
                    key="Steam_123",
                    name="Steam Function",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2,3",
                    value_map={"0": "Off", "1": "Low", "2": "Medium", "3": "High"},
                    read_write="RW",
                ),
                "Steam_shot": DeviceAttribute(
                    key="Steam_shot",
                    name="Steam Shot",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "Water_tank": DeviceAttribute(
                    key="Water_tank",
                    name="Water Tank Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2",
                    value_map={"0": "Empty", "1": "Low", "2": "Full"},
                    read_write="R",
                ),
                # Light and Display
                "Interior_light": DeviceAttribute(
                    key="Interior_light",
                    name="Interior Light",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "Brightness": DeviceAttribute(
                    key="Brightness",
                    name="Display Brightness",
                    attr_type="Number",
                    step=1,
                    value_range="0~5",
                    read_write="RW",
                ),
                "Display_standby": DeviceAttribute(
                    key="Display_standby",
                    name="Display Standby",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Active", "1": "Standby"},
                    read_write="RW",
                ),
                # Meat Probe
                "Meat_probe_status": DeviceAttribute(
                    key="Meat_probe_status",
                    name="Meat Probe Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Not Inserted", "1": "Inserted"},
                    read_write="R",
                ),
                "Meat_probe_set_temperature": DeviceAttribute(
                    key="Meat_probe_set_temperature",
                    name="Meat Probe Target Temperature",
                    attr_type="Number",
                    step=1,
                    value_range="30~100",
                    read_write="RW",
                ),
                "Meat_probe_measured_temperature": DeviceAttribute(
                    key="Meat_probe_measured_temperature",
                    name="Meat Probe Current Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                # Alarms (read-only status indicators)
                "Alarm_baking_finished": DeviceAttribute(
                    key="Alarm_baking_finished",
                    name="Baking Finished Alarm",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                "Alarm_set_temperature_reached": DeviceAttribute(
                    key="Alarm_set_temperature_reached",
                    name="Target Temperature Reached",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                "Alarm_door_opened": DeviceAttribute(
                    key="Alarm_door_opened",
                    name="Door Opened Alert",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                "Alarm_water_tank_is_empty": DeviceAttribute(
                    key="Alarm_water_tank_is_empty",
                    name="Water Tank Empty Alert",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                "Alarm_fast_preheating_finished": DeviceAttribute(
                    key="Alarm_fast_preheating_finished",
                    name="Fast Preheat Finished",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "No", "1": "Yes"},
                    read_write="R",
                ),
                # Grill Plate
                "Grill_plate_status": DeviceAttribute(
                    key="Grill_plate_status",
                    name="Grill Plate Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2",
                    value_map={"0": "Off", "1": "Heating", "2": "Ready"},
                    read_write="R",
                ),
                "Grill_plate_measured_temperature": DeviceAttribute(
                    key="Grill_plate_measured_temperature",
                    name="Grill Plate Temperature",
                    attr_type="Number",
                    read_write="R",
                ),
                # Additional Functions
                "Night_mode_status": DeviceAttribute(
                    key="Night_mode_status",
                    name="Night Mode",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "Gratin_status": DeviceAttribute(
                    key="Gratin_status",
                    name="Gratin Function",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Off", "1": "On"},
                    read_write="RW",
                ),
                "Volume": DeviceAttribute(
                    key="Volume",
                    name="Sound Volume",
                    attr_type="Number",
                    step=1,
                    value_range="0~5",
                    read_write="RW",
                ),
                "Remote_control_monitoring": DeviceAttribute(
                    key="Remote_control_monitoring",
                    name="Remote Control Enabled",
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
