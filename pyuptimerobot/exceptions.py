"""Uptime Robot exceptions."""


class UptimeRobotException(Exception):
    """Base Uptime Robot exception."""


class UptimeRobotConnectionException(UptimeRobotException):
    """Uptime Robot connection exception."""


class UptimeRobotAuthenticationException(UptimeRobotException):
    """Uptime Robot authentication exception."""
