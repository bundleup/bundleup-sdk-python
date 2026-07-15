# BundleUp SDK Tests

This directory contains comprehensive tests for the BundleUp Python SDK.

## Test Suite Overview

The test suite includes **87 tests** covering all major components of the SDK:

### Test Files

1. **conftest.py** - Pytest configuration and shared fixtures
   - API key fixtures
   - Connection ID fixtures
   - Mock response fixtures

2. **test_bundleup.py** (10 tests) - Main BundleUp class
   - Initialization with/without API key
   - Proxy client creation
   - Unify client creation
   - Resource access (connection, integration, webhook)

3. **test_proxy.py** (15 tests) - Proxy API client
   - Initialization and headers
   - URL building
   - HTTP methods (GET, POST, PUT, PATCH, DELETE)
   - Custom headers support
   - Query parameters

4. **test_connection.py** (14 tests) - Connection resource
   - List connections with/without parameters
   - Retrieve specific connection
   - Delete connection
   - Error handling (missing ID, not found)
   - URL building

5. **test_integration.py** (13 tests) - Integration resource
   - List integrations with/without parameters
   - Retrieve specific integration
   - Error handling (unauthorized, server errors)
   - URL building

6. **test_webhook.py** (20 tests) - Webhook resource
   - List webhooks
   - Create webhooks with/without secret
   - Retrieve webhooks
   - Update webhooks (full and partial)
   - Delete webhooks
   - Error handling
   - URL building

7. **test_unify.py** (15 tests) - Unify API client
   - Unify class initialization
   - Chat, Git, and Ticketing subclients
   - Method signatures and parameters
   - Base class configuration

## Running Tests

### Run all tests:

```bash
python3 -m pytest tests/ -v
```

### Run specific test file:

```bash
python3 -m pytest tests/test_proxy.py -v
```

### Run tests with short traceback:

```bash
python3 -m pytest tests/ -v --tb=short
```

### Run specific test class:

```bash
python3 -m pytest tests/test_bundleup.py::TestBundleUpInitialization -v
```

### Run specific test:

```bash
python3 -m pytest tests/test_bundleup.py::TestBundleUpInitialization::test_init_with_api_key -v
```

## Test Coverage

The test suite covers:

- ✅ Initialization and configuration
- ✅ All HTTP methods (GET, POST, PUT, PATCH, DELETE)
- ✅ Query parameters and custom headers
- ✅ Error handling and validation (exceptions for non-2xx responses)
- ✅ URL building and routing
- ✅ Resource CRUD operations
- ✅ Client instantiation patterns
- ✅ JSON response parsing

## SDK API Behavior

The SDK has been updated to follow these patterns:

### Successful Responses

- Methods return JSON data directly (dict/list)
- No need to call `.json()` on responses

### Error Responses

- Non-2xx responses raise `Exception` with error details
- Tests use `pytest.raises()` to verify error handling

### Delete Operations

- 204 No Content responses return `None`
- 404 and other errors raise exceptions

## Dependencies

The tests require the following packages (specified in requirements-dev.txt):

- pytest>=7.0.0
- pytest-mock>=3.10.0
- responses>=0.22.0

Install dev dependencies:

```bash
pip install -r requirements-dev.txt
```

## Fixtures

### Shared Fixtures (conftest.py)

- `api_key` - Test API key string
- `connection_id` - Test connection ID
- `integration_id` - Test integration ID
- `webhook_id` - Test webhook ID
- `mock_responses` - Activated responses mock for HTTP requests

## Test Structure

Tests are organized into classes by functionality:

- Initialization tests
- List/retrieve operations
- Create/update/delete operations
- URL building tests
- Error handling tests

Each test is:

- **Isolated** - Uses mocked HTTP responses
- **Documented** - Includes docstrings explaining purpose
- **Fast** - No real API calls
- **Reliable** - Deterministic and repeatable

## Bug Fixes Made During Test Development

1. Fixed `_resource_name` property decorator in resource classes
2. Fixed URL building with trailing slashes for proper path construction
3. Fixed `_delete` method to handle 204 No Content responses (returns `None` instead of trying to parse empty body)
4. Updated base class methods to return JSON directly instead of response objects
5. Updated base class to raise exceptions for non-2xx responses, making error handling more straightforward

## Notes

- All tests use the `responses` library to mock HTTP requests
- No actual API calls are made during testing
- Tests verify both success and error scenarios
- All 87 tests pass successfully ✅
