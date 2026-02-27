# BundleUp Python SDK

[![PyPI version](https://badge.fury.io/py/bundleup-sdk.svg)](https://badge.fury.io/py/bundleup-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python versions](https://img.shields.io/pypi/pyversions/bundleup-sdk.svg)](https://pypi.org/project/bundleup-sdk/)

Official Python SDK for the [BundleUp](https://bundleup.io) API. Connect to 100+ integrations with a single, unified API. Build once, integrate everywhere.

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Features](#features)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Core Concepts](#core-concepts)
- [API Reference](#api-reference)
  - [Connections](#connections)
  - [Integrations](#integrations)
  - [Webhooks](#webhooks)
  - [Proxy API](#proxy-api)
  - [Unify API](#unify-api)
- [Error Handling](#error-handling)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Installation

Install the SDK using pip:

```bash
pip install bundleup-sdk
```

**Using Poetry:**

```bash
poetry add bundleup-sdk
```

**Using pipenv:**

```bash
pipenv install bundleup-sdk
```

## Requirements

- **Python**: 3.8 or higher
- **requests**: >=2.25.0 (automatically installed)
- **typing-extensions**: >=4.0.0 (automatically installed)

### Python Compatibility

The BundleUp SDK is tested and supported on:

- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

## Features

- 🚀 **Pythonic API** - Follows Python best practices and PEP 8
- 📦 **Easy Integration** - Simple, intuitive API design
- ⚡ **Async Support** - Built on requests with async capabilities
- 🔌 **100+ Integrations** - Connect to Slack, GitHub, Jira, Linear, and many more
- 🎯 **Unified API** - Consistent interface across all integrations via Unify API
- 🔑 **Proxy API** - Direct access to underlying integration APIs
- 🪶 **Lightweight** - Minimal dependencies
- 🛡️ **Error Handling** - Comprehensive error messages and validation
- 📚 **Well Documented** - Extensive documentation and examples
- 🔍 **Type Hints** - Full type annotations for better IDE support
- 🧪 **Tested** - Comprehensive test suite with pytest

## Quick Start

Get started with BundleUp in just a few lines of code:

```python
from bundleup import BundleUp
import os

# Initialize the client
client = BundleUp(os.environ['BUNDLEUP_API_KEY'])

# List all active connections
connections = client.connection.list()
print(f"You have {len(connections)} active connections")

# Use the Proxy API to make requests to integrated services
proxy = client.proxy('conn_123')
response = proxy.get('/api/users')
users = response.json()
print(f"Users: {users}")

# Use the Unify API for standardized data across integrations
unify = client.unify('conn_456')
channels = unify.chat.channels({'limit': 10})
print(f"Chat channels: {channels['data']}")
```

## Authentication

The BundleUp SDK uses API keys for authentication. You can obtain your API key from the [BundleUp Dashboard](https://app.bundleup.io).

### Getting Your API Key

1. Sign in to your [BundleUp Dashboard](https://app.bundleup.io)
2. Navigate to **API Keys**
3. Click **Create API Key**
4. Copy your API key and store it securely

### Initializing the SDK

```python
from bundleup import BundleUp

# Initialize with API key
client = BundleUp('your_api_key_here')

# Or use environment variable (recommended)
import os
client = BundleUp(os.environ['BUNDLEUP_API_KEY'])

# Or use python-dotenv
from dotenv import load_dotenv
load_dotenv()
client = BundleUp(os.getenv('BUNDLEUP_API_KEY'))
```

### Security Best Practices

- ✅ **DO** store API keys in environment variables
- ✅ **DO** use a secrets management service in production
- ✅ **DO** rotate API keys regularly
- ❌ **DON'T** commit API keys to version control
- ❌ **DON'T** hardcode API keys in your source code
- ❌ **DON'T** share API keys in public channels

**Example `.env` file:**

```bash
BUNDLEUP_API_KEY=bu_live_1234567890abcdefghijklmnopqrstuvwxyz
```

**Loading environment variables:**

Install python-dotenv:

```bash
pip install python-dotenv
```

Then in your application:

```python
from dotenv import load_dotenv
import os

load_dotenv()

from bundleup import BundleUp
client = BundleUp(os.getenv('BUNDLEUP_API_KEY'))
```

**For Django applications:**

```python
# settings.py
import os
from pathlib import Path

BUNDLEUP_API_KEY = os.environ.get('BUNDLEUP_API_KEY')

# views.py or services
from django.conf import settings
from bundleup import BundleUp

client = BundleUp(settings.BUNDLEUP_API_KEY)
```

**For Flask applications:**

```python
# config.py
import os

class Config:
    BUNDLEUP_API_KEY = os.environ.get('BUNDLEUP_API_KEY')

# app.py
from flask import Flask
from bundleup import BundleUp

app = Flask(__name__)
app.config.from_object('config.Config')
client = BundleUp(app.config['BUNDLEUP_API_KEY'])
```

## Core Concepts

### Platform API

The **Platform API** provides access to core BundleUp features like managing connections and integrations. Use this API to list, retrieve, and delete connections, as well as discover available integrations.

### Proxy API

The **Proxy API** allows you to make direct HTTP requests to the underlying integration's API through BundleUp. This is useful when you need access to integration-specific features not covered by the Unify API.

### Unify API

The **Unify API** provides a standardized, normalized interface across different integrations. For example, you can fetch chat channels from Slack, Discord, or Microsoft Teams using the same API call.

## API Reference

### Connections

Manage your integration connections.

#### List Connections

Retrieve a list of all connections in your account.

```python
connections = client.connection.list()
```

**With query parameters:**

```python
connections = client.connection.list({
    'integration_id': 'int_slack',
    'limit': 50,
    'offset': 0,
    'external_id': 'user_123'
})
```

**Query Parameters:**

- `integration_id` (str): Filter by integration ID
- `integration_identifier` (str): Filter by integration identifier (e.g., 'slack', 'github')
- `external_id` (str): Filter by external user/account ID
- `limit` (int): Maximum number of results (default: 50, max: 100)
- `offset` (int): Number of results to skip for pagination

**Response:**

```python
[
    {
        'id': 'conn_123abc',
        'external_id': 'user_456',
        'integration_id': 'int_slack',
        'is_valid': True,
        'created_at': '2024-01-15T10:30:00Z',
        'updated_at': '2024-01-20T14:22:00Z',
        'refreshed_at': '2024-01-20T14:22:00Z',
        'expires_at': '2024-04-20T14:22:00Z'
    },
    # ... more connections
]
```

#### Retrieve a Connection

Get details of a specific connection by ID.

```python
connection = client.connection.retrieve('conn_123abc')
```

**Response:**

```python
{
    'id': 'conn_123abc',
    'external_id': 'user_456',
    'integration_id': 'int_slack',
    'is_valid': True,
    'created_at': '2024-01-15T10:30:00Z',
    'updated_at': '2024-01-20T14:22:00Z',
    'refreshed_at': '2024-01-20T14:22:00Z',
    'expires_at': '2024-04-20T14:22:00Z'
}
```

#### Delete a Connection

Remove a connection from your account.

```python
client.connection.delete('conn_123abc')
```

**Note:** Deleting a connection will revoke access to the integration and cannot be undone.

### Integrations

Discover and work with available integrations.

#### List Integrations

Get a list of all available integrations.

```python
integrations = client.integration.list()
```

**With query parameters:**

```python
integrations = client.integration.list({
    'status': 'active',
    'limit': 100,
    'offset': 0
})
```

**Query Parameters:**

- `status` (str): Filter by status ('active', 'inactive', 'beta')
- `limit` (int): Maximum number of results
- `offset` (int): Number of results to skip for pagination

**Response:**

```python
[
    {
        'id': 'int_slack',
        'identifier': 'slack',
        'name': 'Slack',
        'category': 'chat',
        'created_at': '2023-01-01T00:00:00Z',
        'updated_at': '2024-01-15T10:00:00Z'
    },
    # ... more integrations
]
```

#### Retrieve an Integration

Get details of a specific integration.

```python
integration = client.integration.retrieve('int_slack')
```

**Response:**

```python
{
    'id': 'int_slack',
    'identifier': 'slack',
    'name': 'Slack',
    'category': 'chat',
    'created_at': '2023-01-01T00:00:00Z',
    'updated_at': '2024-01-15T10:00:00Z'
}
```

### Webhooks

Manage webhook subscriptions for real-time event notifications.

#### List Webhooks

Get all registered webhooks.

```python
webhooks = client.webhook.list()
```

**With pagination:**

```python
webhooks = client.webhook.list({
    'limit': 50,
    'offset': 0
})
```

**Response:**

```python
[
    {
        'id': 'webhook_123',
        'name': 'My Webhook',
        'url': 'https://example.com/webhook',
        'events': {
            'connection.created': True,
            'connection.deleted': True
        },
        'created_at': '2024-01-15T10:30:00Z',
        'updated_at': '2024-01-20T14:22:00Z',
        'last_triggered_at': '2024-01-20T14:22:00Z'
    }
]
```

#### Create a Webhook

Register a new webhook endpoint.

```python
webhook = client.webhook.create({
    'name': 'Connection Events Webhook',
    'url': 'https://example.com/webhook',
    'events': {
        'connection.created': True,
        'connection.deleted': True,
        'connection.updated': True
    }
})
```

**Webhook Events:**

- `connection.created` - Triggered when a new connection is established
- `connection.deleted` - Triggered when a connection is removed
- `connection.updated` - Triggered when a connection is modified

**Request Body:**

- `name` (str): Friendly name for the webhook
- `url` (str): Your webhook endpoint URL
- `events` (dict): Events to subscribe to

**Response:**

```python
{
    'id': 'webhook_123',
    'name': 'Connection Events Webhook',
    'url': 'https://example.com/webhook',
    'events': {
        'connection.created': True,
        'connection.deleted': True,
        'connection.updated': True
    },
    'created_at': '2024-01-15T10:30:00Z',
    'updated_at': '2024-01-15T10:30:00Z'
}
```

#### Retrieve a Webhook

Get details of a specific webhook.

```python
webhook = client.webhook.retrieve('webhook_123')
```

#### Update a Webhook

Modify an existing webhook.

```python
updated = client.webhook.update('webhook_123', {
    'name': 'Updated Webhook Name',
    'url': 'https://example.com/new-webhook',
    'events': {
        'connection.created': True,
        'connection.deleted': False
    }
})
```

#### Delete a Webhook

Remove a webhook subscription.

```python
client.webhook.delete('webhook_123')
```

#### Webhook Payload Example

When an event occurs, BundleUp sends a POST request to your webhook URL with the following payload:

```json
{
  "id": "evt_1234567890",
  "type": "connection.created",
  "created_at": "2024-01-15T10:30:00Z",
  "data": {
    "id": "conn_123abc",
    "external_id": "user_456",
    "integration_id": "int_slack",
    "is_valid": true,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Webhook Security (Flask Example)

To verify webhook signatures in a Flask application:

```python
from flask import Flask, request, jsonify
import hmac
import hashlib
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('Bundleup-Signature')
    payload = request.get_data()

    if not verify_signature(payload, signature):
        return jsonify({'error': 'Invalid signature'}), 401

    event = request.get_json()
    process_webhook_event(event)

    return '', 200

def verify_signature(payload: bytes, signature: str) -> bool:
    secret = os.environ['BUNDLEUP_WEBHOOK_SECRET']
    computed = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed, signature)

def process_webhook_event(event: dict):
    event_type = event['type']

    if event_type == 'connection.created':
        handle_connection_created(event['data'])
    elif event_type == 'connection.deleted':
        handle_connection_deleted(event['data'])
    elif event_type == 'connection.updated':
        handle_connection_updated(event['data'])
    elif event_type == 'connection.expired':
        handle_connection_expired(event['data'])
```

**Django Example:**

```python
# views.py
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import hmac
import hashlib
import json

@csrf_exempt
def bundleup_webhook(request):
    if request.method != 'POST':
        return HttpResponseForbidden()

    signature = request.META.get('HTTP_BUNDLEUP_SIGNATURE')
    payload = request.body

    if not verify_signature(payload, signature):
        return HttpResponseForbidden('Invalid signature')

    event = json.loads(payload)
    process_webhook_event(event)

    return HttpResponse(status=200)

def verify_signature(payload: bytes, signature: str) -> bool:
    secret = settings.BUNDLEUP_WEBHOOK_SECRET
    computed = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed, signature)
```

### Proxy API

Make direct HTTP requests to integration APIs through BundleUp.

#### Creating a Proxy Instance

```python
proxy = client.proxy('conn_123abc')
```

#### GET Request

```python
response = proxy.get('/api/users')
data = response.json()
print(data)
```

**With query parameters:**

```python
response = proxy.get('/api/users', params={'limit': 10})
```

**With custom headers:**

```python
response = proxy.get('/api/users', headers={
    'X-Custom-Header': 'value',
    'Accept': 'application/json'
})
```

#### POST Request

```python
response = proxy.post('/api/users', body={
    'name': 'John Doe',
    'email': 'john@example.com',
    'role': 'developer'
})

new_user = response.json()
print(f"Created user: {new_user}")
```

**With custom headers:**

```python
response = proxy.post(
    '/api/users',
    body={'name': 'John Doe'},
    headers={
        'Content-Type': 'application/json',
        'X-API-Version': '2.0'
    }
)
```

#### PUT Request

```python
response = proxy.put('/api/users/123', body={
    'name': 'Jane Doe',
    'email': 'jane@example.com'
})

updated_user = response.json()
```

#### PATCH Request

```python
response = proxy.patch('/api/users/123', body={
    'email': 'newemail@example.com'
})

partially_updated = response.json()
```

#### DELETE Request

```python
response = proxy.delete('/api/users/123')

if response.ok:
    print('User deleted successfully')
```

#### Working with Response Objects

The Proxy API returns requests Response objects:

```python
response = proxy.get('/api/users')

# Access response body as JSON
data = response.json()

# Check status code
print(response.status_code)  # 200

# Check if successful
print(response.ok)  # True

# Access headers
print(response.headers['content-type'])

# Access raw content
content = response.content

# Access text
text = response.text

# Handle errors
try:
    response = proxy.get('/api/invalid')
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"Request failed: {e}")
```

### Unify API

Access unified, normalized data across different integrations with a consistent interface.

#### Creating a Unify Instance

```python
unify = client.unify('conn_123abc')
```

#### Chat API

The Chat API provides a unified interface for chat platforms like Slack, Discord, and Microsoft Teams.

##### List Channels

Retrieve a list of channels from the connected chat platform.

```python
result = unify.chat.channels({
    'limit': 100,
    'after': None,
    'include_raw': False
})

print(f"Channels: {result['data']}")
print(f"Next cursor: {result['metadata']['next']}")
```

**Parameters:**

- `limit` (int, optional): Maximum number of channels to return (default: 100, max: 1000)
- `after` (str, optional): Pagination cursor from previous response
- `include_raw` (bool, optional): Include raw API response from the integration (default: False)

**Response:**

```python
{
    'data': [
        {
            'id': 'C1234567890',
            'name': 'general'
        },
        {
            'id': 'C0987654321',
            'name': 'engineering'
        }
    ],
    'metadata': {
        'next': 'cursor_abc123'  # Use this for pagination
    },
    '_raw': {  # Only present if include_raw=True
        # Original response from the integration API
    }
}
```

**Pagination example:**

```python
all_channels = []
cursor = None

while True:
    result = unify.chat.channels({
        'limit': 100,
        'after': cursor
    })

    all_channels.extend(result['data'])
    cursor = result['metadata']['next']

    if cursor is None:
        break

print(f"Fetched {len(all_channels)} total channels")
```

#### Git API

The Git API provides a unified interface for version control platforms like GitHub, GitLab, and Bitbucket.

##### List Repositories

```python
result = unify.git.repos({
    'limit': 50,
    'after': None,
    'include_raw': False
})

print(f"Repositories: {result['data']}")
```

**Response:**

```python
{
    'data': [
        {
            'id': '123456',
            'name': 'my-awesome-project',
            'full_name': 'organization/my-awesome-project',
            'description': 'An awesome project',
            'url': 'https://github.com/organization/my-awesome-project',
            'created_at': '2023-01-15T10:30:00Z',
            'updated_at': '2024-01-20T14:22:00Z',
            'pushed_at': '2024-01-20T14:22:00Z'
        }
    ],
    'metadata': {
        'next': 'cursor_xyz789'
    }
}
```

##### List Pull Requests

```python
result = unify.git.pulls('organization/repo-name', {
    'limit': 20,
    'after': None,
    'include_raw': False
})

print(f"Pull Requests: {result['data']}")
```

**Parameters:**

- `repo_name` (str, required): Repository name in the format 'owner/repo'
- `limit` (int, optional): Maximum number of PRs to return
- `after` (str, optional): Pagination cursor
- `include_raw` (bool, optional): Include raw API response

**Response:**

```python
{
    'data': [
        {
            'id': '12345',
            'number': 42,
            'title': 'Add new feature',
            'description': 'This PR adds an awesome new feature',
            'draft': False,
            'state': 'open',
            'url': 'https://github.com/org/repo/pull/42',
            'user': 'john-doe',
            'created_at': '2024-01-15T10:30:00Z',
            'updated_at': '2024-01-20T14:22:00Z',
            'merged_at': None
        }
    ],
    'metadata': {
        'next': None
    }
}
```

##### List Tags

```python
result = unify.git.tags('organization/repo-name', {'limit': 50})

print(f"Tags: {result['data']}")
```

**Response:**

```python
{
    'data': [
        {
            'name': 'v1.0.0',
            'commit_sha': 'abc123def456'
        },
        {
            'name': 'v0.9.0',
            'commit_sha': 'def456ghi789'
        }
    ],
    'metadata': {
        'next': None
    }
}
```

##### List Releases

```python
result = unify.git.releases('organization/repo-name', {'limit': 10})

print(f"Releases: {result['data']}")
```

**Response:**

```python
{
    'data': [
        {
            'id': '54321',
            'name': 'Version 1.0.0',
            'tag_name': 'v1.0.0',
            'description': 'Initial release with all the features',
            'prerelease': False,
            'url': 'https://github.com/org/repo/releases/tag/v1.0.0',
            'created_at': '2024-01-15T10:30:00Z',
            'released_at': '2024-01-15T10:30:00Z'
        }
    ],
    'metadata': {
        'next': None
    }
}
```

#### Project Management API

The PM API provides a unified interface for project management platforms like Jira, Linear, and Asana.

##### List Issues

```python
result = unify.pm.issues({
    'limit': 100,
    'after': None,
    'include_raw': False
})

print(f"Issues: {result['data']}")
```

**Response:**

```python
{
    'data': [
        {
            'id': 'PROJ-123',
            'url': 'https://jira.example.com/browse/PROJ-123',
            'title': 'Fix login bug',
            'status': 'in_progress',
            'description': 'Users are unable to log in',
            'created_at': '2024-01-15T10:30:00Z',
            'updated_at': '2024-01-20T14:22:00Z'
        }
    ],
    'metadata': {
        'next': 'cursor_def456'
    }
}
```

**Filtering and sorting:**

```python
open_issues = [issue for issue in result['data'] if issue['status'] == 'open']
sorted_by_date = sorted(
    result['data'],
    key=lambda x: x['created_at'],
    reverse=True
)
```

## Error Handling

The SDK raises exceptions for errors. Always wrap SDK calls in try-except blocks for proper error handling.

```python
try:
    connections = client.connection.list()
except Exception as e:
    print(f"Failed to fetch connections: {e}")
```

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/bundleup/bundleup-sdk-python.git
cd bundleup-sdk-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Or using requirements files
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=bundleup --cov-report=html

# Run type checker
mypy bundleup

# Run linter
flake8 bundleup
black bundleup --check

# Format code
black bundleup
```

### Project Structure

```
bundleup/
├── __init__.py              # Main entry point
├── proxy.py                 # Proxy API implementation
├── resources/
│   ├── base.py              # Base resource class
│   ├── connection.py        # Connections API
│   ├── integration.py       # Integrations API
│   └── webhook.py           # Webhooks API
└── unify/
    ├── __init__.py          # Unify client wrapper
    ├── base.py              # Base Unify class
    ├── chat.py              # Chat Unify API
    ├── git.py               # Git Unify API
    └── pm.py                # PM Unify API
tests/                       # Test files
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_proxy.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=bundleup

# Run with coverage report
pytest --cov=bundleup --cov-report=html
open htmlcov/index.html

# Run specific test
pytest tests/test_proxy.py::TestProxy::test_get_request
```

### Building and Publishing

```bash
# Build the package
python -m build

# Check the distribution
twine check dist/*

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

### Code Quality Tools

```bash
# Black (code formatter)
black bundleup

# isort (import sorter)
isort bundleup

# flake8 (linter)
flake8 bundleup

# mypy (type checker)
mypy bundleup

# pylint (static analyzer)
pylint bundleup

# Run all checks
black bundleup && isort bundleup && flake8 bundleup && mypy bundleup
```

## Contributing

We welcome contributions to the BundleUp Python SDK! Here's how you can help:

### Reporting Bugs

1. Check if the bug has already been reported in [GitHub Issues](https://github.com/bundleup/bundleup-sdk-python/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Package version and Python version

### Suggesting Features

1. Open a new issue with the "feature request" label
2. Describe the feature and its use case
3. Explain why this feature would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch: `git checkout -b feature/my-new-feature`
3. Make your changes
4. Write or update tests
5. Ensure all tests pass: `pytest`
6. Run code quality checks: `black bundleup && flake8 bundleup`
7. Commit your changes: `git commit -am 'Add new feature'`
8. Push to the branch: `git push origin feature/my-new-feature`
9. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guide
- Add type hints to all functions
- Write docstrings for all public APIs
- Add tests for new features
- Update documentation for API changes
- Keep commits focused and atomic
- Write clear commit messages

## License

This package is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).

```
Copyright (c) 2026 BundleUp

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Support

Need help? We're here for you!

### Documentation

- **Official Docs**: [https://docs.bundleup.io](https://docs.bundleup.io)
- **API Reference**: [https://docs.bundleup.io/api](https://docs.bundleup.io/api)
- **SDK Guides**: [https://docs.bundleup.io/sdk/python](https://docs.bundleup.io/sdk/python)

### Community

- **Discord**: [https://discord.gg/bundleup](https://discord.gg/bundleup)
- **GitHub Discussions**: [https://github.com/bundleup/bundleup-sdk-python/discussions](https://github.com/bundleup/bundleup-sdk-python/discussions)
- **Stack Overflow**: Tag your questions with `bundleup`

### Direct Support

- **Email**: [support@bundleup.io](mailto:support@bundleup.io)
- **GitHub Issues**: [https://github.com/bundleup/bundleup-sdk-python/issues](https://github.com/bundleup/bundleup-sdk-python/issues)
- **Twitter**: [@bundleup_io](https://twitter.com/bundleup_io)

### Enterprise Support

For enterprise customers, we offer:

- Priority support with SLA
- Dedicated support channel
- Architecture consultation
- Custom integration assistance

Contact [enterprise@bundleup.io](mailto:enterprise@bundleup.io) for more information.

## Code of Conduct

Everyone interacting in the BundleUp project's codebases, issue trackers, chat rooms and mailing lists is expected to follow the [code of conduct](https://github.com/bundleup/bundleup-sdk-python/blob/main/CODE_OF_CONDUCT).

---

Made with ❤️ by the [BundleUp](https://bundleup.io) team
