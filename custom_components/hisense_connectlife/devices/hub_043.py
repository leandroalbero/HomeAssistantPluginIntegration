"""Parser for Hub/Controller devices (043 series)."""

from typing import Dict

from .base import BaseDeviceParser, DeviceAttribute


class HubController043Parser(BaseDeviceParser):
    """Parser for Hub/Controller device type 043.

    This device type appears to be a control unit or bridge/hub that manages
    other devices in the system (like the ATW heat pump controller).

    From the API data, this device typically has minimal direct status but
    acts as a coordinator for connected devices.
    """

    @property
    def device_type(self) -> str:
        return "043"

    @property
    def feature_code(self) -> str:
        return ""

    @property
    def attributes(self) -> Dict[str, DeviceAttribute]:
        if not hasattr(self, "_attributes"):
            self._attributes = {
                # Basic online status (usually derived from offlineState)
                "online_status": DeviceAttribute(
                    key="online_status",
                    name="Online Status",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Offline", "1": "Online"},
                    read_write="R",
                ),
                # Device info
                "bindTime": DeviceAttribute(
                    key="bindTime",
                    name="Binding Time",
                    attr_type="Number",
                    read_write="R",
                ),
                "useTime": DeviceAttribute(
                    key="useTime",
                    name="Last Usage Time",
                    attr_type="Number",
                    read_write="R",
                ),
                "createTime": DeviceAttribute(
                    key="createTime",
                    name="Device Creation Time",
                    attr_type="Number",
                    read_write="R",
                ),
                # Room assignment
                "roomId": DeviceAttribute(
                    key="roomId", name="Room ID", attr_type="Number", read_write="RW"
                ),
                "roomName": DeviceAttribute(
                    key="roomName",
                    name="Room Name",
                    attr_type="String",
                    read_write="RW",
                ),
                # Device identification
                "deviceFeatureCode": DeviceAttribute(
                    key="deviceFeatureCode",
                    name="Feature Code",
                    attr_type="String",
                    read_write="R",
                ),
                "deviceFeatureName": DeviceAttribute(
                    key="deviceFeatureName",
                    name="Feature Name",
                    attr_type="String",
                    read_write="R",
                ),
                # Energy monitoring role
                "energyRole": DeviceAttribute(
                    key="energyRole",
                    name="Energy Monitoring Role",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2",
                    value_map={"0": "None", "1": "Monitor", "2": "Controller"},
                    read_write="R",
                ),
                # Visibility flag
                "isShow": DeviceAttribute(
                    key="isShow",
                    name="Visible in App",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1",
                    value_map={"0": "Hidden", "1": "Visible"},
                    read_write="RW",
                ),
                # Role (user permissions)
                "role": DeviceAttribute(
                    key="role",
                    name="User Role",
                    attr_type="Enum",
                    step=1,
                    value_range="0,1,2",
                    value_map={"0": "Owner", "1": "Admin", "2": "Guest"},
                    read_write="R",
                ),
            }
        return self._attributes

    @attributes.setter
    def attributes(self, value: Dict[str, DeviceAttribute]):
        self._attributes = value
