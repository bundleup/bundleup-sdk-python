# BundleUp Python SDK

[![PyPI version](https://badge.fury.io/py/bundleup-sdk.svg)](https://badge.fury.io/py/bundleup-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python versions](https://img.shields.io/pypi/pyversions/bundleup-sdk.svg)](https://pypi.org/project/bundleup-sdk/)

Official Python SDK for the [BundleUp](https://bundleup.io) API. Connect to 100+ integrations with a single, unified API. Build once, integrate everywhere.

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Features](#features)
- [Examples](#examples)
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
- 🤖 **MCP** - Hand a connection to any MCP client, or to OpenAI and Anthropic's hosted MCP
- 🪶 **Lightweight** - Minimal dependencies
- 🛡️ **Error Handling** - Comprehensive error messages and validation
- 📚 **Well Documented** - Extensive documentation and examples
- 🔍 **Type Hints** - Full type annotations for better IDE support
- 🧪 **Tested** - Comprehensive test suite with pytest

## Examples

Runnable examples are available in the [`examples/`](./examples) directory:

- [`examples/basic_usage.py`](./examples/basic_usage.py) - Client setup, connections, integrations, and webhooks
- [`examples/proxy_api.py`](./examples/proxy_api.py) - Proxy API GET request with a connection
- [`examples/unify_api.py`](./examples/unify_api.py) - Unify Chat, Git, Ticketing, CRM, Drive, and Calendar endpoint usage
- [`examples/README.md`](./examples/README.md) - Setup and execution instructions

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
BUNDLEUP_API_KEY=Zw7Lt7JacsDyMCEpnZdGptgnJaOdMzFVH9QtIthnL5RviYP5WeH6e9FWP2HzEO
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

### Auth API

The **Auth API** runs the hosted authorization flow: build the URL that sends a user to connect an integration, then exchange the one-time `code` from the redirect for a `connection_id`. See [Authorization Flow](https://docs.bundleup.io/authorization-flow).

### Platform API

The **Platform API** provides access to core BundleUp features like managing connections and integrations. Use this API to list, retrieve, and delete connections, as well as discover available integrations.

### Proxy API

The **Proxy API** allows you to make direct HTTP requests to the underlying integration's API through BundleUp. This is useful when you need access to integration-specific features not covered by the Unify API.

### Unify API

The **Unify API** provides a standardized, normalized interface across different integrations. For example, you can fetch chat channels from Slack, Discord, or Microsoft Teams using the same API call.

### MCP API

The **MCP API** reaches a provider's own MCP server using a connection's stored credentials. Tools are defined by the provider, not by BundleUp. Because the connection is chosen per client, one agent can serve many end users without ever handling a token.

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
    signature = request.headers.get('BundleUp-Signature')
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

### Auth API

Connect an end user's account and get back a `connection_id`. See [Authorization Flow](https://docs.bundleup.io/authorization-flow) for the full flow.

#### Build the Authorization URL

```python
url = client.auth.build_authorization_url(
    client_id='your-client-id',
    integration_id='github',
    redirect_uri='https://app.example.com/callback',
    external_id='user_42',  # optional
    state='random-csrf-token'  # optional
)

# Redirect the user to `url`
```

**Parameters:**

- `client_id` (str, required): Your workspace client ID
- `integration_id` (str, required): The integration to connect
- `redirect_uri` (str, required): Must exactly match a redirect URI registered in your dashboard
- `external_id` (str, optional): Your own reference, stored on the connection
- `state` (str, optional): Returned unchanged on the redirect

#### Exchange the Code for a Connection

BundleUp redirects back to `redirect_uri` with a one-time `code`. Exchange it server-side:

```python
connection = client.auth.get_connection_from_code(
    code=request.args['code'],
    redirect_uri='https://app.example.com/callback'
)

print(connection['connection_id'])
```

**Parameters:**

- `code` (str, required): The `code` query parameter from the redirect
- `redirect_uri` (str, required): The same redirect URI used to build the authorization URL

**Response:**

```python
{
    'connection_id': 'conn_abc123',
    'external_id': 'user_42',
    'integration_id': 'github'
}
```

The code expires after 5 minutes and can only be exchanged once. An invalid, expired or reused code raises an `Exception` that includes the API's error body. Missing arguments raise `ValueError`.

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

##### List Users

Retrieve a list of users from the connected chat platform.

```python
result = unify.chat.users({
    'limit': 100,
    'after': None,
    'include_raw': False
})

print(f"Users: {result['data']}")
print(f"Next cursor: {result['metadata']['next']}")
```

**Parameters:**

- `limit` (int, optional): Maximum number of users to return (default: 100, max: 1000)
- `after` (str, optional): Pagination cursor from previous response
- `include_raw` (bool, optional): Include raw API response from the integration (default: False)

**Response:**

```python
{
    'data': [
        {
            'id': 'U1234567890',
            'name': 'Jane Doe'
        }
    ],
    'metadata': {
        'next': 'cursor_abc123'
    }
}
```

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

##### List Messages

Messages in one channel, newest first. `author.name` is None on Slack, which returns only a user id on a message.

```python
result = unify.chat.messages('C123', {
    'limit': 100,
    'after': None,
    'include_raw': False
})

print(f"Messages: {result['data']}")
```

**Response:**

```python
{
    'data': [
        {
            'id': '1755712345.123456',
            'text': 'Deploy finished',
            'author': {'id': 'U024BE7LH', 'name': None},
            'created_at': '2026-08-20T18:32:25.123Z',
            'thread_id': None
        }
    ],
    'metadata': {
        'next': 'cursor_def456'
    }
}
```

##### Send Message

Send a message to a channel on the connected chat platform.

```python
result = unify.chat.message('C1234567890', 'Hello from BundleUp! :wave:')

print(f"Message sent: {result['data']}")
```

**Parameters:**

- `channel_id` (str, required): The ID of the channel to send the message to
- `text` (str, required): Markdown-formatted message text

**Response:**

```python
{
    'data': {
        # Raw response data from the chat provider
    }
}
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

##### List Issues

```python
result = unify.git.issues('organization/repo-name', {'limit': 20})

print(f"Issues: {result['data']}")
```

**Response:**

```python
{
    'data': [
        {
            'id': 67890,
            'number': 17,
            'title': 'Timestamps drift on retry',
            'description': 'Retried requests report the first attempt time',
            'state': 'open',
            'url': 'https://github.com/org/repo/issues/17',
            'user': 'john-doe',
            'created_at': '2024-01-15T10:30:00Z',
            'updated_at': '2024-01-20T14:22:00Z',
            'closed_at': None
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

##### List Branches

```python
result = unify.git.branches('organization/repo-name', {'limit': 50})

print(f"Branches: {result['data']}")
```

**Response:**

```python
{
    'data': [
        {
            'name': 'main',
            'commit_sha': 'abc123def456',
            'protected': True
        }
    ],
    'metadata': {
        'next': None
    }
}
```

##### List Commits

```python
result = unify.git.commits('organization/repo-name', {'branch': 'main', 'limit': 20})

print(f"Commits: {result['data']}")
```

`branch` is optional and accepts a branch name, tag or commit SHA. When it is omitted the
provider's default branch is used.

**Response:**

```python
{
    'data': [
        {
            'sha': 'abc123def4567890abc123def4567890abc123de',
            'message': 'Add commits endpoint',
            'url': 'https://github.com/org/repo/commit/abc123def4567890abc123def4567890abc123de',
            'author': 'Jane Doe',
            'author_email': 'jane@example.com',
            'committed_at': '2024-01-15T10:30:00Z'
        }
    ],
    'metadata': {
        'next': None
    }
}
```

#### Ticketing API

The Ticketing API provides a unified interface for ticketing and project management platforms like Jira, Linear, and Asana.

##### List Tickets

```python
result = unify.ticketing.tickets({
    'limit': 100,
    'after': None,
    'include_raw': False
})

print(f"Tickets: {result['data']}")
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
open_tickets = [ticket for ticket in result['data'] if ticket['status'] == 'open']
sorted_by_date = sorted(
    result['data'],
    key=lambda x: x['created_at'],
    reverse=True
)
```

##### Get a Ticket

Fetch one ticket by ID. Not supported by Basecamp, whose API only serves a to-do underneath its project.

```python
result = unify.ticketing.ticket('PROJ-123')

print(f"Ticket: {result['data']}")
```

**Response:**

```python
{
    'data': {
        'id': 'PROJ-123',
        'url': 'https://jira.example.com/browse/PROJ-123',
        'title': 'Fix login bug',
        'status': 'in_progress',
        'description': 'Users are unable to log in',
        'created_at': '2024-01-15T10:30:00Z',
        'updated_at': '2024-01-20T14:22:00Z'
    }
}
```

A single resource carries no pagination, so there is no `metadata` on this response.

##### List Projects

```python
result = unify.ticketing.projects({
    'limit': 100,
    'after': None,
    'include_raw': False
})

print(f"Projects: {result['data']}")
```

**Response:**

```python
{
    'data': [
        {
            'id': '10001',
            'name': 'Website Redesign',
            'status': 'active',
            'url': 'https://jira.example.com/browse/PROJ',
            'description': 'All the work for the new marketing site',
            'created_at': '2024-01-15T10:30:00Z',
            'updated_at': '2024-01-20T14:22:00Z'
        }
    ],
    'metadata': {
        'next': 'cursor_def456'
    }
}
```

**Note:** Not every platform returns every field. Jira does not expose creation or update timestamps for projects, so `created_at` and `updated_at` are `None` for Jira connections, and `status` is only set when Jira reports whether the project is archived.

#### CRM API

The CRM API provides a unified interface for CRM platforms like Attio, HubSpot, PipeDrive, Salesforce and Zoho.

##### List Companies

```python
result = unify.crm.companies({
    'limit': 100,
    'after': None,
    'include_raw': False
})

print(f"Companies: {result['data']}")
```

**Response:**

```python
{
    'data': [
        {
            'id': '12345',
            'name': 'Acme Inc.',
            'website': 'https://acme.example.com'
        }
    ],
    'metadata': {
        'next': None
    }
}
```

##### List Contacts

```python
result = unify.crm.contacts({
    'limit': 100,
    'after': None,
    'include_raw': False
})

print(f"Contacts: {result['data']}")
```

**Response:**

```python
{
    'data': [
        {
            'id': '67890',
            'name': 'Jane Doe',
            'email': 'jane@acme.example.com'
        }
    ],
    'metadata': {
        'next': None
    }
}
```

#### Drive API

The Drive API provides a unified interface for file storage platforms like Google Drive, OneDrive, Box, Dropbox and Microsoft SharePoint.

##### List Files

```python
result = unify.drive.files({
    'limit': 100,
    'after': None,
    'include_raw': False
})

print(f"Files: {result['data']}")
```

**Response:**

```python
{
    'data': [
        {
            'id': 'file_123',
            'name': 'quarterly-report.pdf',
            'mime_type': 'application/pdf',
            'size': 204800,
            'created_at': '2024-01-15T10:30:00Z',
            'updated_at': '2024-01-20T14:22:00Z',
            'url': 'https://drive.example.com/file_123',
            'is_folder': False
        }
    ],
    'metadata': {
        'next': None
    }
}
```

#### Calendar API

The Calendar API provides a unified interface for calendar and scheduling platforms like Google Calendar, Outlook, Calendly and Zoom.

##### List Events

`starts_after` and `starts_before` are required — the endpoint refuses an unbounded listing.

```python
result = unify.calendar.events({
    'starts_after': '2026-09-01T00:00:00Z',
    'starts_before': '2026-09-08T00:00:00Z',
    'limit': 100,
    'after': None,
    'include_raw': False
})

print(f"Events: {result['data']}")
```

**Response:**

```python
{
    'data': [
        {
            'id': 'evt_123',
            'title': 'Design review',
            'description': 'Walk through the new onboarding flow',
            'start_date': '2026-09-01T15:00:00Z',
            'end_date': '2026-09-01T16:00:00Z',
            'status': 'confirmed',
            'url': 'https://calendar.google.com/event?eid=...'
        }
    ],
    'metadata': {
        'next': None
    }
}
```

Recurring events are expanded into their occurrences. All-day events carry a `YYYY-MM-DD` date rather than a timestamp. Attendees, conferencing links and organizers are available through `include_raw` or the Proxy API.

### MCP API

Reach a provider's own MCP server using a connection's credentials. BundleUp injects and refreshes the access token, so the connection ID is the only thing your agent needs to know about a user.

Supported for providers that run a first-party MCP server — see the [integrations page](https://www.bundleup.io/integrations). Others return an `mcp_not_supported` error.

BundleUp does not ship an MCP client. Hand `hosted()` or `transport()` to the one you already use, or send JSON-RPC yourself with `post` and `delete`, which return the response untouched as `requests.Response` objects, like the Proxy API.

#### Creating an MCP Instance

```python
mcp = client.mcp('conn_123abc')
```

#### Model-Hosted MCP

OpenAI and Anthropic can connect to an MCP server themselves, with no tool mapping or dispatch loop on your side. Both accept only a single credential and no custom headers, so `hosted()` returns the server URL alongside the API key and connection joined into one bearer.

```python
hosted = client.mcp('conn_123abc').hosted()

response = openai.responses.create(
    model='gpt-4o',
    input='What issues are assigned to me?',
    tools=[
        {
            'type': 'mcp',
            'server_label': 'linear',
            'server_url': hosted['url'],
            'authorization': hosted['token'],
            'require_approval': 'never',
        }
    ],
)
```

Anthropic's connector takes the same pair as `url` and `authorization_token`.

`server_url` must be exactly the URL `hosted()` returns — the proxy rebuilds the upstream URL from the provider's own base, so any path or query you append is ignored rather than rejected.

This sends your API key to the model provider, whose servers make the request. Use an MCP client in your own backend if that is not acceptable.

#### Using an MCP Client Library

`transport()` returns the URL and headers if you would rather use an existing MCP client, such as the official [`mcp`](https://pypi.org/project/mcp/) package.

```python
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

transport = client.mcp('conn_123abc').transport()

async with streamablehttp_client(transport['url'], headers=transport['headers']) as (read, write, _):
    async with ClientSession(read, write) as session:
        await session.initialize()
        result = await session.list_tools()
```

#### Sending JSON-RPC Directly

MCP requires an `initialize` handshake before any other method. The session ID comes back on that first response and must be sent on every call after it.

```python
mcp = client.mcp('conn_123abc')

# 1. Handshake
init = mcp.post({
    'jsonrpc': '2.0',
    'id': 1,
    'method': 'initialize',
    'params': {
        'protocolVersion': '2025-06-18',
        'capabilities': {},
        'clientInfo': {'name': 'my-agent', 'version': '1.0.0'},
    },
})

session_id = init.headers.get('mcp-session-id')
session = {'Mcp-Session-Id': session_id} if session_id else {}

# 2. Confirm the handshake (a notification — no id, no response body)
mcp.post({'jsonrpc': '2.0', 'method': 'notifications/initialized'}, session)

# 3. List tools
response = mcp.post({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'}, session)
result = parse(response)['result']

print(result['tools'])
```

Providers may answer with `text/event-stream` rather than JSON, so responses need unwrapping either way:

```python
import json

def parse(response):
    if 'text/event-stream' not in response.headers.get('content-type', ''):
        return response.json()

    data = '\n'.join(
        line[5:].strip() for line in response.text.splitlines() if line.startswith('data:')
    )

    return json.loads(data)
```

Tool lists can be paginated. If `result['nextCursor']` is set, call `tools/list` again with `'params': {'cursor': result['nextCursor']}` until it comes back empty.

Calling a tool follows the same shape:

```python
response = mcp.post({
    'jsonrpc': '2.0',
    'id': 3,
    'method': 'tools/call',
    'params': {'name': 'create_issue', 'arguments': {'title': 'Login broken'}},
}, session)
```

#### Sessions

MCP sessions live on the provider's server — BundleUp holds no session state. Close one when you are done:

```python
mcp.delete({'Mcp-Session-Id': session_id})
```

#### Errors

BundleUp rejects a request before it reaches the provider by returning an HTTP error with a JSON body — the response is passed straight through, so check `response.ok` yourself.

```python
response = mcp.post(body)

if not response.ok:
    error = response.json()
    # connection_invalid, connection_refresh_failed, mcp_not_supported, rate_limit
    print(error['code'], error['message'])
```

Every JSON-RPC message counts toward the rate limit of 100 requests per 60 seconds, per connection — including the `initialize` handshake.

#### Several Connections

An agent often needs more than one provider for the same end user. With model-hosted MCP there is nothing to merge — pass one `mcp` tool per connection and the model provider keeps them apart by `server_label`:

```python
connections = {'slack': user.slack_connection, 'linear': user.linear_connection}

tools = []

for label, connection_id in connections.items():
    hosted = client.mcp(connection_id).hosted()

    tools.append({
        'type': 'mcp',
        'server_label': label,
        'server_url': hosted['url'],
        'authorization': hosted['token'],
        'require_approval': 'never',
    })
```

With an MCP client in your own backend, open one client per connection from its `transport()`, prefix each tool name with a label (`slack__send_message`), and route calls back by that prefix. There is no merge helper in the SDK — how tools are namespaced, filtered and recovered from differs enough per agent that it is better written where you can see it.

**Filter before you hand tools to a model** — three providers is easily sixty tools, and accuracy drops as that list grows, so give the agent only the ones it needs.

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
├── auth.py                  # Auth API (authorization URL + code exchange)
├── proxy.py                 # Proxy API implementation
├── mcp.py                   # MCP API (transport + hosted)
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
    ├── ticketing.py         # Ticketing Unify API
    ├── crm.py               # CRM Unify API
    ├── drive.py             # Drive Unify API
    ├── calendar.py          # Calendar Unify API
    └── types.py             # TypedDicts for Unify response shapes
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

## Code of Conduct

Everyone interacting in the BundleUp project's codebases, issue trackers, chat rooms and mailing lists is expected to follow the [code of conduct](https://github.com/bundleup/bundleup-sdk-python/blob/main/CODE_OF_CONDUCT).

---

Made with ❤️ by the [BundleUp](https://bundleup.io) team
