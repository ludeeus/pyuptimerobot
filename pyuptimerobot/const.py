"""Uptime Robot constants."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

API_BASE_URL = "https://api.uptimerobot.com/v2"
API_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

ATTR_URL = "url"
