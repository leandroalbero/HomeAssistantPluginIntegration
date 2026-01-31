"""Constants for the ConnectLife standalone client."""

from typing import Final

# Import configuration from environment
from .config import (
    CLIENT_ID,
    CLIENT_SECRET,
    OAUTH2_CALLBACK_URL,
    OAUTH2_AUTHORIZE,
    OAUTH2_TOKEN,
    API_BASE_URL,
    WEBSOCKET_URL,
    TOKEN_FILE,
    LOG_LEVEL,
)

DOMAIN = "hisense_connectlife"

# API Endpoints
API_DEVICE_LIST = "/clife-svc/pu/get_device_status_list"
API_GET_PROPERTY_LTST = "/clife-svc/get_property_list"
API_QUERY_STATIC_DATA = "/clife-svc/pu/query_static_data"
API_DEVICE_CONTROL = "/device/pu/property/set"
API_SELF_CHECK = "/basic/self_check/info"
API_GET_HOUR_POWER = "/clife-svc/pu/get_hour_power"

# Token settings
TOKEN_EXPIRY_MARGIN = 60  # seconds before token expiry to refresh

# Update interval
UPDATE_INTERVAL = 30  # seconds

# Temperature settings
MIN_TEMP = 16
MAX_TEMP = 30
MIN_TEMP_WATER = 16
MAX_TEMP_WATER = 30


# Status Keys
class StatusKey:
    """Status keys for device properties."""

    POWER = "t_power"
    MODE = "t_work_mode"
    FAN_SPEED = "t_fan_speed"
    TEMPERATURE = "f_temp_in"
    T_TEMP_TYPE = "t_temp_type"
    FHUMIDITY = "f_humidity"
    WATER_TANK_TEMP = "f_water_tank_temp"
    DHW_TEMP = "t_dhw_temp"
    ZONE1WATER_TEMP1 = "f_zone1water_temp1"
    ZONE1WATER_SETTEMP1 = "t_zone1water_settemp1"
    ZONE2WATER_TEMP2 = "f_zone2water_temp2"
    CONSUMPTION = "f_power_consumption"
    IN_WATER_TEMP = "f_in_water_temp"
    OUT_WATER_TEMP = "f_out_water_temp"
    ELECTRIC_HEATING = "f_electric_heating"
    TARGET_TEMP = "t_temp"
    HUMIDITY = "t_humidity"
    SWING = "t_up_down"
    QUIET = "t_fan_mute"
    RAPID = "t_super"
    EIGHTHEAT = "t_8heat"
    ECO = "t_eco"
    ENERGY = "f_electricity"
    WATER_TEMP = "t_water_temp"
    ZONE_TEMP = "t_zone_temp"
