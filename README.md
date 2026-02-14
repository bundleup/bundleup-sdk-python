# BundleUp Python SDK

[![PyPI version](https://badge.fury.io/py/bundleup-sdk.svg)](https://badge.fury.io/py/bundleup-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for the BundleUp API.

## Installation

```bash
pip install bundleup-sdk
```

## Features

- **Pythonic API Design** - Context managers, property decorators, and Python best practices
- **Custom Exception Hierarchy** - Specific exception types for different error scenarios
- **Connection Pooling** - Efficient HTTP connection reuse with `requests.Session`
- **Type Hints** - Full type annotation support for better IDE integration
- **Comprehensive Testing** - 70+ unit tests with mocked HTTP requests

## Usage

### Initialize the Client

The SDK supports both regular initialization and context manager usage:

```python
from bundleup import BundleUp

# Regular usage
client = BundleUp("your-api-key")

# Context manager (automatically closes connections)
with BundleUp("your-api-key") as client:
    connections = client.connections.list()
```

### Working with Connections

```python
# List all connections
connections = client.connections.list()

# Create a new connection
connection = client.connections.create({
    "name": "My Connection",
    "integration_id": "integration-id"
})

# Retrieve a specific connection
connection = client.connections.retrieve("connection-id")

# Delete a connection
client.connections.delete("connection-id")
```

### Working with Integrations

```python
# List all integrations
integrations = client.integrations.list()

# Retrieve a specific integration
integration = client.integrations.retrieve("integration-id")
```

### Working with Webhooks

```python
# List all webhooks
webhooks = client.webhooks.list()

# Create a new webhook
webhook = client.webhooks.create({
    "url": "https://example.com/webhook",
    "events": ["connection.created"]
})

# Update a webhook
updated = client.webhooks.update("webhook-id", {
    "url": "https://example.com/new-webhook"
})

# Delete a webhook
client.webhooks.delete("webhook-id")
```

### Using the Proxy API

```python
# Create a proxy instance
proxy = client.proxy("connection-id")

# Make requests to the connected service
response = proxy.get("/users")
response = proxy.post("/users", {"name": "John"})
response = proxy.put("/users/123", {"name": "Jane"})
response = proxy.patch("/users/123", {"email": "jane@example.com"})
response = proxy.delete("/users/123")
```

### Using the Unify API

The Unify API provides a standardized interface across different integrations.

#### Chat

```python
# Get unified chat channels
channels = client.unify("connection-id").chat.channels()

# With pagination parameters
channels = client.unify("connection-id").chat.channels({
    "limit": 50,
    "include_raw": True
})
```

#### Git

```python
unify = client.unify("connection-id")

# Get repositories
repos = unify.git.repos()

# Get pull requests
pulls = unify.git.pulls()

# Get tags
tags = unify.git.tags()

# Get releases
releases = unify.git.releases()
```

#### Project Management

```python
# Get issues
issues = client.unify("connection-id").pm.issues()

# With pagination
issues = client.unify("connection-id").pm.issues({
    "limit": 100,
    "after": "cursor-id"
})
```

## Error Handling

The SDK uses a hierarchy of custom exceptions:

```python
from bundleup import BundleUp
from bundleup.exceptions import (
    BundleUpError,          # Base exception
    ValidationError,        # Input validation errors
    APIError,              # General API errors
    AuthenticationError,   # 401 errors
    NotFoundError,        # 404 errors
    RateLimitError        # 429 errors
)

try:
    client = BundleUp("your-api-key")
    connections = client.connections.list()
except AuthenticationError:
    print("Invalid API key")
except NotFoundError:
    print("Resource not found")
except RateLimitError:
    print("Rate limit exceeded")
except APIError as e:
    print(f"API error: {e.status_code} - {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
```

## Advanced Usage

### Custom Session

You can provide your own `requests.Session` for advanced configuration:

```python
import requests
from bundleup import BundleUp

session = requests.Session()
session.timeout = 30
session.verify = True

client = BundleUp("your-api-key", session=session)
```

### Query Parameters

The `list()` method supports query parameters:

```python
# List with filters
connections = client.connections.list(status="active", limit=50)
```

## Requirements

- Python 3.8+
- requests
- typing-extensions

## License

MIT License - see LICENSE file for details.

## Documentation

For more information, visit [https://docs.bundleup.io](https://docs.bundleup.io)
