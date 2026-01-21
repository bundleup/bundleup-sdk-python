# BundleUp Python SDK

Official Python SDK for the BundleUp API.

## Installation

```bash
pip install bundleup-sdk
```

## Usage

### Initialize the Client

```python
from bundleup import BundleUp

client = BundleUp("your-api-key")
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

# Update a connection
updated = client.connections.update("connection-id", {
    "name": "Updated Name"
})

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
```

## Requirements

- Python 3.8+
- requests
- typing-extensions

## License

MIT License - see LICENSE file for details.

## Documentation

For more information, visit [https://docs.bundleup.io](https://docs.bundleup.io)
