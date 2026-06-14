# Copilot instructions for pyuptimerobot

`pyuptimerobot` is an async Python wrapper for the Uptime Robot **v3** API. It exposes a small `UptimeRobot` client for fetching account details and managing monitors.

These instructions are shared with Claude Code via a root `CLAUDE.md` symlink. Keep them accurate: when the repository changes (structure, tooling, commands, or public API), update this file in the same change.

## Project facts

- **Python**: 3.14+ (`.python-version`, `pyproject.toml`).
- **Runtime dependency**: `aiohttp` only.
- **Build backend**: `hatchling`.
- **Dependency / task runner**: `uv`. Development tasks are wrapped in the `scripts/` directory ("Scripts to Rule Them All"). Prefer the wrappers over raw commands.

## Development workflow

- **Setup**: `scripts/setup` (delegates to `scripts/bootstrap` → `uv sync --dev --all-extras`).
- **Test**: `scripts/test` — runs `pytest` with coverage.
- **Lint + format** (mutating): `scripts/lint` — `ruff format`, then `ruff check --fix`, then `mypy pyuptimerobot`.
- **Lint check** (non-mutating, matches CI): `scripts/lint-check`.
- **Coverage**: `scripts/coverage` — coverage must stay at 100%.
- **Build**: `scripts/build` — `uv build`.

## Repository structure

- `pyuptimerobot/` — package source.
  - `__init__.py` — public exports.
  - `uptimerobot.py` — the `UptimeRobot` API client.
  - `models.py` — dataclass models with a `from_dict` classmethod.
  - `exceptions.py` — exception hierarchy.
  - `const.py` — base URL, expected status codes, logger.
  - `py.typed` — typing marker.
- `tests/` — pytest suite, with `common.py` helpers and JSON `fixtures/`.
- `scripts/` — development scripts.
- `example.py` — usage example.

There is no `decorator.py` and no `@endpoint` decorator.

## Client conventions

- Construct with keyword arguments: `UptimeRobot(api_key=..., session=...)`.
- Public methods are `async def async_*` and return `UptimeRobotApiResponse[...]`:
  `async_get_monitors`, `async_get_account_details`, `async_edit_monitor`,
  `async_pause_monitor`, `async_start_monitor`, `async_reset_monitor`.
- All requests route through the private `_call_api(...)`, which takes an `api_path`, an HTTP `method`, optional `json`, and a `data_transformer` callable that maps the raw response into a model. It uses bearer-token auth and a 10 second timeout.
- Base URL is `https://api.uptimerobot.com/v3` (`API_BASE_URL` in `const.py`).
- Error handling maps to: `UptimeRobotAuthenticationException` (HTTP 401), `UptimeRobotConnectionException` (other non-success statuses, `ClientError`, timeouts), and `UptimeRobotException` (base class / unexpected errors).

### Adding an endpoint

1. Add an `async_*` method that delegates to `_call_api` with the correct `api_path`, `method`, and `data_transformer`.
2. Add or extend models in `models.py`.
3. Add a JSON fixture under `tests/fixtures/`.
4. Add a test covering success and failure.
5. Keep coverage at 100%.

## Testing

- `pytest` with `pytest-asyncio` (`asyncio_mode = "strict"`).
- Mock all HTTP with `aresponses`; never make real network calls.
- Load fixtures via `tests.common.fixture(...)` and use `tests.common.TEST_API_TOKEN`.
- Tests are organized per endpoint; error and edge cases live in `tests/test_issues.py`.

Example:

```python
import aiohttp
import pytest

from pyuptimerobot import UptimeRobot, UptimeRobotAccount
from tests.common import TEST_API_TOKEN, TEST_RESPONSE_HEADERS, fixture


@pytest.mark.asyncio
async def test_async_get_account_details(aresponses):
    aresponses.add(
        "api.uptimerobot.com",
        "/v3/user/me",
        "get",
        aresponses.Response(
            text=fixture("getAccountDetails", False),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )
    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(api_key=TEST_API_TOKEN, session=session)
        result = await client.async_get_account_details()
        assert isinstance(result.data, UptimeRobotAccount)
```

## Style

- Formatting and linting via `ruff` (line length 99, target `py314`; import sorting uses `combine-as-imports` and `force-sort-within-sections`).
- Type checking via `mypy` in strict mode; use full type hints.
- Keep inline comments **and** docstrings to an absolute minimum. Do not add them unless explicitly requested.

## Markdown conventions

- Put a blank line before and after every heading.
- Use ATX-style headings (`#`).
- Use backticks for code, filenames, and technical terms.

## Completion checklist

Before considering a change complete:

1. `scripts/lint-check` is clean.
2. `scripts/test` passes.
3. Coverage is 100% (`scripts/coverage`).
