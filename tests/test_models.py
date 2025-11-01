"""Tests for models."""

from pyuptimerobot.models import UptimeRobotApiResponse


def test_api_response_unknown_endpoint():
    """Test UptimeRobotApiResponse.from_dict with unknown API path (fallback)."""
    data = {
        "_api_path": "/unknown/endpoint",
        "_method": "GET",
        "some_key": "some_value",
        "another_key": 123,
    }

    result = UptimeRobotApiResponse.from_dict(data)

    assert result._api_path == "/unknown/endpoint"
    assert result._method == "GET"
    assert result.data == {"some_key": "some_value", "another_key": 123}
    assert result.pagination is None
