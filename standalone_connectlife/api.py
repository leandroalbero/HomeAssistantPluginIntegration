"""API client for ConnectLife."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import re
import time
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Callable

import aiohttp

from .const import (
    API_BASE_URL,
    API_DEVICE_LIST,
    API_GET_PROPERTY_LTST,
    API_QUERY_STATIC_DATA,
    API_DEVICE_CONTROL,
    API_GET_HOUR_POWER,
    API_SELF_CHECK,
    CLIENT_ID,
    CLIENT_SECRET,
)
from .device_parsers import get_device_parser, BaseDeviceParser, BaseBeanParser
from .models import DeviceInfo
from .exceptions import ApiError

_LOGGER = logging.getLogger(__name__)


class ConnectLifeApiClient:
    """ConnectLife API client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        oauth_session: Any,
    ) -> None:
        """Initialize API client."""
        self.failed_data: Dict[str, List[str]] = {}
        self.oauth_session = oauth_session
        self.session = session
        self._devices: Dict[str, DeviceInfo] = {}
        self.parsers: Dict[str, BaseDeviceParser] = {}
        self.static_data: Dict[str, Any] = {}
        self._status_callbacks: Dict[str, Callable[[Dict[str, Any]], None]] = {}
        self._source_id: Optional[str] = None

    def calculate_signature_sha256(self, secret: str, params: str) -> str:
        """Calculate HMAC SHA256 signature."""
        return base64.b64encode(
            hmac.new(
                bytes(secret, "utf-8"), bytes(params, "utf-8"), hashlib.sha256
            ).digest()
        ).decode("utf-8")

    def calculate_body_digest_sha256(self, body: Optional[Dict]) -> str:
        """Calculate body digest."""
        if body and len(body) > 0:
            return base64.b64encode(
                hashlib.sha256(json.dumps(body).encode("utf-8")).digest()
            ).decode("utf-8")
        return "47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="

    def calculate_GMT_date(self) -> str:
        """Calculate GMT date string."""
        GMT_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
        return datetime.utcnow().strftime(GMT_FORMAT)

    def calculate_path(self, url: str) -> str:
        """Calculate path from URL."""
        return re.sub(r"^https://[^/]*", "", url)

    def calculate_encrypt(
        self, secret_key: str, method: str, path: str, gmt_date: str, header: str
    ) -> str:
        """Calculate encryption string."""
        return f"{secret_key}\n{method} {path}\ndate: {gmt_date}\n{header}\n"

    def _generate_uuid(self) -> str:
        """Generate a UUID string without dashes."""
        return f"{uuid.uuid1().hex}{int(time.time() * 1000)}"

    def _get_source_id(self) -> str:
        """Get or generate source ID."""
        if not self._source_id:
            uuid_str = self._generate_uuid()
            md5_uuid = hashlib.md5(uuid_str.encode()).hexdigest()
            self._source_id = f"td001002000{md5_uuid}"
        return self._source_id

    async def _api_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Dict:
        """Make an API request."""
        _LOGGER.debug("Making API request: %s %s", method, endpoint)
        try:
            # Ensure token is valid
            await self.oauth_session.async_ensure_token_valid()

            # Get system parameters
            params = await self._get_system_parameters()
            _LOGGER.debug("System parameters: %s", json.dumps(params, indent=2))

            # Merge with provided data
            request_data = data if data else {}
            request_data.update(params)

            if headers is None:
                headers = {}

            # Add accessToken to headers only for GET requests
            if method.upper() == "GET":
                headers.update(
                    {"accessToken": await self.oauth_session.async_get_access_token()}
                )

            # Build full URL
            url = f"{API_BASE_URL}{endpoint}"

            # For GET requests, append parameters to URL
            if method.upper() == "GET":
                query_params = []
                url_params = request_data.copy()
                url_params.pop("accessToken", None)

                for key, value in url_params.items():
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value)
                    query_params.append(f"{key}={value}")
                query_string = "&".join(query_params)
                url = f"{url}?{query_string}"
                request_data = None

            app_id = CLIENT_ID
            app_secret = CLIENT_SECRET
            header_key = "hi-params-encrypt"
            gmt_date = self.calculate_GMT_date()
            params_str = self.calculate_encrypt(
                app_id,
                method,
                self.calculate_path(url),
                gmt_date,
                f"{header_key}: {app_id}",
            )

            sign = self.calculate_signature_sha256(app_secret, params_str)

            # Prepare headers
            headers.update(
                {
                    f"{header_key}": f"{app_id}",
                    "Date": gmt_date,
                    "Authorization": f'Signature signature="{sign}", keyId="{app_id}",algorithm="hmac-sha256", headers="@request-target date {header_key}"',
                    "Content-Type": "application/json",
                    "Digest": f"SHA-256={self.calculate_body_digest_sha256(request_data)}",
                }
            )

            # Log request details
            _LOGGER.debug("Request URL: %s", url)
            _LOGGER.debug("Request Method: %s", method)
            _LOGGER.debug(
                "Request Headers: %s",
                {
                    k: v if k.lower() != "accesstoken" else "***"
                    for k, v in headers.items()
                },
            )
            if request_data:
                _LOGGER.debug("Request Body: %s", json.dumps(request_data, indent=2))

            # Convert request_data to JSON string for POST requests
            json_data = json.dumps(request_data) if request_data else None

            async with self.session.request(
                method, url, data=json_data, headers=headers
            ) as resp:
                response_text = await resp.text()

                _LOGGER.debug("Response Status: %d", resp.status)
                _LOGGER.debug("Response Body: %s", response_text)

                resp.raise_for_status()

                try:
                    response_data = json.loads(response_text)
                except json.JSONDecodeError as err:
                    _LOGGER.error("Failed to parse response as JSON: %s", err)
                    raise ApiError(f"Invalid JSON response: {response_text}")

                if not isinstance(response_data, dict):
                    raise ApiError(f"Unexpected response format: {response_data}")

                if response_data.get("resultCode") != 0:
                    error_msg = response_data.get("msg", "Unknown error")
                    raise ApiError(f"API error: {error_msg}")

                return response_data

        except aiohttp.ClientError as err:
            _LOGGER.error("HTTP request failed: %s", err)
            raise ApiError(f"HTTP request failed: {err}")
        except Exception as err:
            _LOGGER.error("API request failed: %s", err)
            raise ApiError(f"API request failed: {err}")

    async def _get_system_parameters(self) -> Dict[str, Any]:
        """Generate system parameters."""
        timestamp = int(time.time() * 1000)
        uuid_str = str(uuid.uuid1()) + str(timestamp)
        random_str = hashlib.md5(uuid_str.encode()).hexdigest()

        params = {
            "timeStamp": str(timestamp),
            "version": "8.1",
            "languageId": "1",
            "timezone": "UTC",
            "randStr": random_str,
            "appId": CLIENT_ID,
            "sourceId": self._get_source_id(),
            "platformId": 5,
        }

        # Add access token if available
        try:
            access_token = await self.oauth_session.async_get_access_token()
            if access_token:
                params["accessToken"] = access_token
        except:
            pass

        return params

    async def async_get_devices(self) -> Dict[str, DeviceInfo]:
        """Get list of devices with their current status."""
        _LOGGER.debug("Fetching device list with status")
        try:
            response = await self._api_request("GET", API_DEVICE_LIST)
            if not response:
                return {}

            devices = {}
            device_list = response.get("deviceList", [])
            _LOGGER.debug("Found %d devices in response", len(device_list))

            for device_data in device_list:
                device_type_code = device_data.get("deviceTypeCode")
                device_feature_code = device_data.get("deviceFeatureCode")

                try:
                    device = DeviceInfo(device_data)
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

                    if device_type_code in supported_device_types:
                        devices[device.device_id] = device
                        self._devices[device.device_id] = device
                        _LOGGER.debug(
                            "Added supported device:\n%s", device.debug_info()
                        )

                        # Get property list for the device
                        try:
                            response_props = await self.async_get_property_list(
                                device_type_code, device_feature_code
                            )
                            property_list = response_props.get("status", [])
                        except Exception as e:
                            _LOGGER.warning("Failed to get property list: %s", e)
                            property_list = []

                        # Get static data if feature code contains "99"
                        if "99" in device_feature_code:
                            try:
                                static_response = await self.async_query_static_data(
                                    device.puid
                                )
                                self.static_data[device.device_id] = (
                                    static_response.get("status", {})
                                )
                            except Exception as e:
                                _LOGGER.warning("Failed to get static data: %s", e)

                        # Get device parser
                        parser_class = get_device_parser(
                            device_type_code, device_feature_code
                        )
                        parser = parser_class()

                        # Filter parser attributes based on property list for bean parsers
                        if isinstance(parser, BaseBeanParser) and property_list:
                            parser = self._create_filtered_parser(parser, property_list)

                        self.parsers[device.device_id] = parser
                        _LOGGER.debug(
                            "Parser for device %s: %s",
                            device.device_id,
                            type(parser).__name__,
                        )

                        # Check for power consumption feature
                        await self._check_power_consumption(
                            device, device_type_code, property_list
                        )

                        # Get self-check/fault data
                        try:
                            self_check_data = await self.async_api_self_check(
                                "1", device.puid
                            )
                            failed_data = self_check_data.get("status", {}).get(
                                "selfCheckFailedList", []
                            )
                            if failed_data:
                                failed_list = [
                                    item.get("statusKey") for item in failed_data
                                ]
                                device.failed_data = failed_list
                        except Exception as e:
                            _LOGGER.debug("Failed to get self-check data: %s", e)

                    else:
                        _LOGGER.warning(
                            "Skipping unsupported device type: %s", device_type_code
                        )

                except Exception as device_err:
                    _LOGGER.error(
                        "Error processing device data: %s - %s", device_data, device_err
                    )

            return devices

        except Exception as err:
            _LOGGER.error("Failed to fetch devices: %s", err)
            raise ApiError(f"Failed to fetch devices: {err}")

    def _create_filtered_parser(
        self, base_parser: BaseBeanParser, property_list: List[Dict]
    ) -> BaseBeanParser:
        """Create a filtered parser based on available properties."""
        from .device_parsers.base import DeviceAttribute

        original_attributes = base_parser.attributes
        property_keys = {
            prop.get("propertyKey") for prop in property_list if "propertyKey" in prop
        }

        filtered_attributes = {}
        for key in property_keys:
            if key in original_attributes:
                attribute = original_attributes[key]

                # Update value_range from property list
                for prop in property_list:
                    if prop.get("propertyKey") == key:
                        property_value_list = prop.get("propertyValueList")
                        if property_value_list:
                            attribute.value_range = property_value_list
                        break

                # Filter value_map
                if attribute.value_map and property_value_list:
                    property_value_list_keys = set(property_value_list.split(","))
                    value_map_keys = set(attribute.value_map.keys())
                    filtered_value_map = {
                        k: attribute.value_map[k]
                        for k in value_map_keys.intersection(property_value_list_keys)
                    }
                    attribute.value_map = filtered_value_map

                filtered_attributes[key] = attribute

        # Add power consumption attribute
        if "f_power_consumption" not in filtered_attributes:
            filtered_attributes["f_power_consumption"] = DeviceAttribute(
                key="f_power_consumption",
                name="Power Consumption",
                attr_type="Number",
                step=1,
                read_write="R",
            )

        # Create new parser with filtered attributes
        new_parser = BaseBeanParser()
        new_parser._attributes = filtered_attributes
        return new_parser

    async def _check_power_consumption(
        self, device: DeviceInfo, device_type_code: str, property_list: List[Dict]
    ) -> None:
        """Check and fetch power consumption data if available."""
        has_power = False
        property_keys = {
            prop.get("propertyKey") for prop in property_list if "propertyKey" in prop
        }

        # Check based on device type
        if device_type_code == "009":  # Split AC
            target_keys = {"f_power_display", "f_cool_qvalue", "f_heat_qvalue"}
            if target_keys & property_keys:
                has_power = True
        elif device_type_code in [
            "008",
            "006",
            "007",
        ]:  # Window, Portable, Dehumidifier
            if "f_power_display" in property_keys:
                has_power = True

        if has_power:
            try:
                current_date = datetime.now().date().isoformat()
                power_response = await self.async_get_hour_power(
                    current_date, device.puid
                )
                power = power_response.get("status", {})

                current_time = datetime.now()
                previous_hour = (current_time - timedelta(hours=1)).hour
                previous_hour_str = str(previous_hour)
                value = power.get(previous_hour_str)

                if value is not None:
                    device.status["f_power_consumption"] = value
                    _LOGGER.debug(
                        "Power consumption for hour %s: %s", previous_hour_str, value
                    )
            except Exception as e:
                _LOGGER.debug("Failed to get power consumption: %s", e)
        else:
            # Remove power consumption attribute if not supported
            if device.device_id in self.parsers:
                self.parsers[device.device_id].remove_attribute("f_power_consumption")

    async def async_get_property_list(
        self, device_type_code: str, device_feature_code: str
    ) -> Dict[str, Any]:
        """Get property list for a device type."""
        params = {
            "deviceTypeCode": device_type_code,
            "deviceFeatureCode": device_feature_code,
        }

        response = await self._api_request("GET", API_GET_PROPERTY_LTST, data=params)

        if response.get("resultCode") == 0:
            return {
                "success": True,
                "status": response.get("properties", []),
            }
        else:
            error_msg = response.get("msg", "Unknown error")
            raise ApiError(f"Failed to get property list: {error_msg}")

    async def async_query_static_data(self, puid: str) -> Dict[str, Any]:
        """Query static data for a device."""
        params = {"puid": puid}

        response = await self._api_request("POST", API_QUERY_STATIC_DATA, data=params)

        if response.get("resultCode") == 0:
            return {
                "success": True,
                "status": response.get("data", {}),
            }
        else:
            error_msg = response.get("msg", "Unknown error")
            raise ApiError(f"Failed to query static data: {error_msg}")

    async def async_get_hour_power(self, date: str, puid: str) -> Dict[str, Any]:
        """Get hourly power consumption."""
        params = {
            "date": date,
            "puid": puid,
        }

        response = await self._api_request("POST", API_GET_HOUR_POWER, data=params)

        if response.get("resultCode") == 0:
            return {
                "success": True,
                "status": response.get("powerConsumption", {}),
            }
        else:
            error_msg = response.get("msg", "Unknown error")
            raise ApiError(f"Failed to get hour power: {error_msg}")

    async def async_api_self_check(self, no_record: str, puid: str) -> Dict[str, Any]:
        """Perform self check on device."""
        params = {
            "noRecord": no_record,
            "puid": puid,
        }

        response = await self._api_request("POST", API_SELF_CHECK, data=params)

        if response.get("resultCode") == 0:
            return {
                "success": True,
                "status": response.get("data", {}),
            }
        else:
            error_msg = response.get("msg", "Unknown error")
            raise ApiError(f"Self check failed: {error_msg}")

    async def async_control_device(
        self, puid: str, properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Control device by setting properties."""
        try:
            params = {
                "puid": puid,
                "properties": properties,
            }

            response = await self._api_request(
                "POST",
                API_DEVICE_CONTROL,
                data=params,
            )

            if response.get("resultCode") == 0:
                return {
                    "success": True,
                    "status": response.get("kvMap", {}),
                }
            else:
                error_msg = response.get("msg", "Unknown error")
                raise ApiError(f"Control failed: {error_msg}")

        except Exception as err:
            raise ApiError(f"Failed to control device: {err}") from err

    def get_device_parser(self, device_id: str) -> Optional[BaseDeviceParser]:
        """Get parser for a device."""
        return self.parsers.get(device_id)

    def parse_device_status(self, device: DeviceInfo) -> Dict[str, Any]:
        """Parse device status using appropriate parser."""
        parser = self.parsers.get(device.device_id)
        if not parser:
            _LOGGER.warning("No parser found for device %s", device.device_id)
            return device.status

        try:
            parsed_status = parser.parse_status(device.status)
            return parsed_status
        except Exception as err:
            _LOGGER.error("Failed to parse status for device %s: %s", device.name, err)
            return device.status

    async def get_device_status(self, device_id: str) -> Dict[str, Any]:
        """Get device status from cached device list."""
        device = self._devices.get(device_id)
        if not device:
            # Refresh device list
            devices = await self.async_get_devices()
            device = devices.get(device_id)
            if not device:
                raise ApiError(f"Device not found: {device_id}")

        return self.parse_device_status(device)
