# Copilot instructions for pyuptimerobot

This is a Python API wrapper for Uptime Robot that provides async methods to interact with the Uptime Robot API for monitoring uptime and managing monitors.

## Project overview

pyuptimerobot is a Python library that wraps the Uptime Robot API, providing an easy-to-use async interface for fetching account details, managing monitors, and handling uptime data. The library is designed to be simple, reliable, and follows modern Python best practices.

## Code standards

### Required before each commit

- Run `scripts/lint` to format code with isort and black
- Run `scripts/test` to ensure all tests pass
- Use the provided scripts in the `scripts/` directory for consistency

### Development workflow

- **Setup**: `scripts/setup` - Install dependencies and set up development environment
- **Test**: `scripts/test` - Run the full test suite with pytest
- **Lint**: `scripts/lint` - Format and lint code (isort + black + mypy)
- **Lint check**: `scripts/lint-check` - Check code formatting without making changes
- **Coverage**: `scripts/coverage` - Generate test coverage reports (must be 100%)
- **Build**: `scripts/build` - Build the package

## Repository structure

- `pyuptimerobot/` - Main package source code
  - `__init__.py` - Package exports
  - `uptimerobot.py` - Main UptimeRobot API client
  - `decorator.py` - Request decorators for API calls
  - `models.py` - Data models for API responses
  - `exceptions.py` - Custom exception classes
  - `const.py` - Constants and configuration
- `tests/` - Test suite using pytest and aresponses
  - `test_*.py` - Test files for different API endpoints
  - `fixtures/` - Test fixtures and mock data
  - `common.py` - Common test utilities
- `scripts/` - Development scripts following "Scripts to Rule Them All" pattern
- `example.py` - Usage examples

## Key development guidelines

### 1. Code style and formatting

- **Python version**: Support Python 3.13+ (as specified in pyproject.toml)
- **Dependencies**: Keep dependencies minimal - currently only aiohttp for runtime
- **Type hints**: Use type hints throughout for better IDE support
- **Docstrings**: Follow Google-style docstrings for classes and public methods
- **Import style**: Keep imports clean and organized (isort handles this)
- **Async/await**: All API methods use async/await pattern

### 2. API client implementation

- Use aiohttp for async HTTP requests
- Apply the `@endpoint` decorator for API endpoint methods
- Handle errors gracefully and provide meaningful exceptions
- Support all Uptime Robot API endpoints consistently

### 3. Testing standards

- **100% coverage required**: All code must have test coverage
- **Mock API responses**: Use aresponses to mock HTTP responses
- **Test fixtures**: Use JSON fixtures in `tests/fixtures/` for response data
- **Edge cases**: Test error scenarios, timeouts, and malformed responses
- **Async testing**: Use pytest-asyncio for async test support

### 4. Error handling

- Use custom exceptions from `exceptions.py`
- Provide clear error messages for API failures
- Handle connection errors, timeouts, and invalid responses
- Validate API responses before processing

### 5. Backwards compatibility

- This library is used in production - maintain API compatibility
- Deprecate features gracefully before removal
- Follow semantic versioning for releases

## Specific implementation patterns

### Adding new API endpoints

1. Add the method to `uptimerobot.py` with `@endpoint` decorator
2. Define response models in `models.py` if needed
3. Add test fixtures in `tests/fixtures/`
4. Create comprehensive tests in `tests/`
5. Update documentation and examples

### Exception handling

```python
from .exceptions import (
    UptimeRobotException,
    UptimeRobotApiKeyException,
    UptimeRobotConnectionException,
)

# Raise specific exceptions for different error types
if api_key_invalid:
    raise UptimeRobotApiKeyException("Invalid API key")
    
if connection_failed:
    raise UptimeRobotConnectionException("Failed to connect to API")
```

### Testing pattern

```python
import pytest
from aresponses import ResponsesMockServer

from pyuptimerobot import UptimeRobot
from tests.common import fixture, TEST_API_TOKEN

@pytest.mark.asyncio
async def test_api_method(aresponses: ResponsesMockServer):
    """Test API method with mock response."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v2/endpoint",
        "POST",
        response=fixture("endpoint_response"),
        status=200,
    )
    
    async with aiohttp.ClientSession() as session:
        api = UptimeRobot(TEST_API_TOKEN, session)
        result = await api.async_method()
        assert result is not None
```

## Testing guidelines

### Running tests

- Use `scripts/test` for full test suite
- Tests must pass and coverage must be 100%
- Use `scripts/coverage` to verify coverage

### Writing tests

- Follow the existing pattern in test files
- Use descriptive test names
- Mock all external API calls with aresponses
- Use fixtures for response data
- Test both success and failure scenarios

## Documentation standards

- Keep README.md updated with usage examples
- Use clear, concise examples that users can copy-paste
- Document any breaking changes in release notes
- Include type information in documentation
- Follow Google's Markdown style guide:
  - **ALWAYS put a blank line before and after headings** - this is mandatory
  - Use ATX-style headings (`#`)
  - Use backticks for code, filenames, and technical terms
  - Use numbered lists for procedures, bullet lists for non-sequential items

## Git workflow

- Use conventional commit messages
- Keep commits focused and atomic
- Include tests with feature additions
- Update documentation for user-facing changes

## Notes for Copilot

- This is an API wrapper - maintain consistency with Uptime Robot API
- All API methods must be async
- Use the `@endpoint` decorator for API methods
- Mock all HTTP requests in tests - no real API calls
- Use the existing script system rather than running commands directly
- Maintain 100% test coverage requirement
- **Do not add inline comments to code unless specifically requested by the user.**

## Completion requirements

Before considering any code generation or changes complete, ensure all of the following pass:

1. **Tests must pass**: Run `scripts/test` - all tests must pass without errors
2. **Linting must be clean**: Run `scripts/lint` - code must be properly formatted and linted
3. **Coverage must be 100%**: Run `scripts/coverage` - test coverage must remain at 100%

Any pull request or code changes that don't meet these requirements should be considered incomplete. If coverage drops below 100%, add the necessary tests to restore full coverage.
