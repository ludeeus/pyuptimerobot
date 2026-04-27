"""Uptime Robot constants."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

API_BASE_URL = "https://api.uptimerobot.com/v3"
ATTR_URL = "url"

API_MONITOR_ACTION_PAUSE = "pause"
API_MONITOR_ACTION_START = "start"

API_PATH_MONITORS = "/monitors"
API_PATH_MONITOR_DETAIL = "/monitors/{monitor_id}"
API_PATH_USER_ME = "/user/me"

API_STATUS_DOWN = "down"
API_STATUS_PAUSED = "paused"
API_STATUS_STARTED = "started"
API_STATUS_UP = "up"

API_STATUS_TO_ACTION: dict[str, str] = {
    API_STATUS_DOWN: API_MONITOR_ACTION_PAUSE,
    API_STATUS_PAUSED: API_MONITOR_ACTION_START,
    API_STATUS_STARTED: API_MONITOR_ACTION_PAUSE,
    API_STATUS_UP: API_MONITOR_ACTION_PAUSE,
}
