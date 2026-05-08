"""Uptime Robot constants."""

from http import HTTPStatus
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

API_BASE_URL = "https://api.uptimerobot.com/v3"

EXPECTED_API_STATUS_CODES = (
    HTTPStatus.OK,
    HTTPStatus.CREATED,
)
