"""Tests for models."""

from pyuptimerobot.models import UptimeRobotApiResponse


def test_api_response_wraps_data_for_arbitrary_api_path():
    """Test UptimeRobotApiResponse.from_dict wraps data and preserves request metadata."""
    data = {
        "some_key": "some_value",
        "another_key": 123,
    }

    result = UptimeRobotApiResponse.from_dict(
        data=data, api_path="/unknown/endpoint", method="GET"
    )

    assert result._api_path == "/unknown/endpoint"
    assert result._method == "GET"
    assert result.data == {"some_key": "some_value", "another_key": 123}
    assert result.pagination is None
