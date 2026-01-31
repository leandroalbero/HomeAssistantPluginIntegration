"""Data models for ConnectLife client."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from .exceptions import ApiError

_LOGGER = logging.getLogger(__name__)


class DeviceInfo:
    """Device information class."""

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize device info."""
        if not isinstance(data, dict):
            _LOGGER.warning("DeviceInfo initialized with non-dict data: %s", data)
            data = {}

        # Basic device information
        self.wifi_id = data.get("wifiId")
        self.device_id = data.get("deviceId")
        self.puid = data.get("puid")
        self.name = data.get("deviceNickName")
        self.feature_code = data.get("deviceFeatureCode")
        self.feature_name = data.get("deviceFeatureName")
        self.type_code = data.get("deviceTypeCode")
        self.type_name = data.get("deviceTypeName")
        self.bind_time = data.get("bindTime")
        self.role = data.get("role")
        self.room_id = data.get("roomId")
        self.room_name = data.get("roomName")
        self._failed_data: List[str] = []

        # Status information
        status_list = data.get("statusList", {})
        if isinstance(status_list, dict):
            self.status = status_list
        else:
            _LOGGER.warning("Invalid status data: %s", status_list)
            self.status = {}

        # Other information
        self.use_time = data.get("useTime")
        self.offline_state = data.get("offlineState")
        self.onOff = self.status.get("t_power")
        self.seq = data.get("seq")
        self.create_time = data.get("createTime")
        self._is_online = self.offline_state == 1
        self._is_onOff = self.onOff == 1 or self.onOff == "1"

        _LOGGER.debug(
            "Device %s (type: %s-%s) onOff: %s, _is_onOff: %s",
            self.feature_code,
            self.type_code,
            self.feature_code,
            self.onOff,
            self._is_onOff,
        )

    @property
    def is_online(self) -> bool:
        """Return if device is online."""
        return self._is_online

    @property
    def failed_data(self) -> List[str]:
        """Property to access failed_data safely."""
        return self._failed_data

    @property
    def is_onOff(self) -> bool:
        """Return if device is on."""
        return self._is_onOff

    def is_supported(self) -> bool:
        """Check if this device type is supported."""
        supported_device_types = [
            "009",
            "008",
            "007",
            "006",
            "016",
            "035",
            "013",
            "044",
            "043",
        ]
        return self.type_code in supported_device_types

    def get_status_value(self, key: str, default: Any = None) -> Any:
        """Get value from status list."""
        return self.status.get(key, default)

    def has_attribute(self, key: str) -> bool:
        """Check if device has a specific attribute."""
        return key in self.status

    def to_dict(self) -> Dict[str, Any]:
        """Convert device info to dictionary."""
        return {
            "wifiId": self.wifi_id,
            "deviceId": self.device_id,
            "puid": self.puid,
            "deviceNickName": self.name,
            "deviceFeatureCode": self.feature_code,
            "deviceFeatureName": self.feature_name,
            "deviceTypeCode": self.type_code,
            "deviceTypeName": self.type_name,
            "bindTime": self.bind_time,
            "role": self.role,
            "roomId": self.room_id,
            "roomName": self.room_name,
            "statusList": self.status,
            "useTime": self.use_time,
            "offlineState": self.offline_state,
            "seq": self.seq,
            "createTime": self.create_time,
        }

    def debug_info(self) -> str:
        """Return detailed debug information about the device."""
        info = [
            f"Device: {self.name} ({self.device_id})",
            f"PUID: {self.puid}",
            f"Type: {self.type_code}-{self.feature_code} ({self.type_name} - {self.feature_name})",
            f"Online: {self.is_online} (offline_state: {self.offline_state})",
            f"Status: {self.status}",
            f"Supported: {self.is_supported()}",
        ]
        return "\n".join(info)

    @failed_data.setter
    def failed_data(self, value: List[str]):
        self._failed_data = value


class DeviceStatus:
    """Device status wrapper."""

    def __init__(self, device: DeviceInfo, parsed_status: Dict[str, Any]) -> None:
        """Initialize device status."""
        self.device = device
        self.parsed = parsed_status

    def get(self, key: str, default: Any = None) -> Any:
        """Get parsed status value."""
        return self.parsed.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {"device": self.device.to_dict(), "status": self.parsed}
