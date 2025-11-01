"""Uptime Robot constants."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

API_BASE_URL = "https://api.uptimerobot.com/v3"
ATTR_URL = "url"

API_PATH_MONITORS = "/monitors"
API_PATH_MONITOR_DETAIL = "/monitors/{monitor_id}"
API_PATH_USER_ME = "/user/me"
