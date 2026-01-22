"""
Example usage of the BundleUp Python SDK.

This script demonstrates how to use the various features of the BundleUp SDK.
Note: This is for demonstration purposes only. You'll need a valid API key
and connection ID to make actual API calls.
"""

from bundleup import BundleUp

# Initialize the client with your API key
client = BundleUp("your-api-key-here")

# ============================================================================
# Working with Connections
# ============================================================================

# List all connections
try:
    connections = client.connections.list()
    print(f"Found {len(connections)} connections")
except Exception as e:
    print(f"Error listing connections: {e}")

# Create a new connection
try:
    new_connection = client.connections.create({
        "name": "My Connection",
        "integration_id": "integration-id"
    })
    print(f"Created connection: {new_connection.get('id')}")
except Exception as e:
    print(f"Error creating connection: {e}")

# Retrieve a specific connection
try:
    connection = client.connections.retrieve("connection-id")
    print(f"Retrieved connection: {connection.get('name')}")
except Exception as e:
    print(f"Error retrieving connection: {e}")

# Update a connection
try:
    updated_connection = client.connections.update("connection-id", {
        "name": "Updated Connection Name"
    })
    print(f"Updated connection: {updated_connection.get('name')}")
except Exception as e:
    print(f"Error updating connection: {e}")

# Delete a connection
try:
    client.connections.delete("connection-id")
    print("Connection deleted successfully")
except Exception as e:
    print(f"Error deleting connection: {e}")

# ============================================================================
# Working with Integrations
# ============================================================================

# List all integrations
try:
    integrations = client.integrations.list()
    print(f"Found {len(integrations)} integrations")
except Exception as e:
    print(f"Error listing integrations: {e}")

# Retrieve a specific integration
try:
    integration = client.integrations.retrieve("integration-id")
    print(f"Retrieved integration: {integration.get('name')}")
except Exception as e:
    print(f"Error retrieving integration: {e}")

# ============================================================================
# Working with Webhooks
# ============================================================================

# List all webhooks
try:
    webhooks = client.webhooks.list()
    print(f"Found {len(webhooks)} webhooks")
except Exception as e:
    print(f"Error listing webhooks: {e}")

# Create a webhook
try:
    webhook = client.webhooks.create({
        "url": "https://example.com/webhook",
        "events": ["connection.created", "connection.updated"]
    })
    print(f"Created webhook: {webhook.get('id')}")
except Exception as e:
    print(f"Error creating webhook: {e}")

# ============================================================================
# Using the Proxy API
# ============================================================================

# Create a proxy for a specific connection
proxy = client.proxy("connection-id")

# Make a GET request
try:
    users = proxy.get("/users")
    print(f"Retrieved users via proxy")
except Exception as e:
    print(f"Error making proxy GET request: {e}")

# Make a POST request
try:
    new_user = proxy.post("/users", {
        "name": "John Doe",
        "email": "john@example.com"
    })
    print(f"Created user via proxy: {new_user.get('id')}")
except Exception as e:
    print(f"Error making proxy POST request: {e}")

# Make a PUT request
try:
    updated_user = proxy.put("/users/123", {
        "name": "Jane Doe"
    })
    print(f"Updated user via proxy")
except Exception as e:
    print(f"Error making proxy PUT request: {e}")

# Make a PATCH request
try:
    patched_user = proxy.patch("/users/123", {
        "email": "jane@example.com"
    })
    print(f"Patched user via proxy")
except Exception as e:
    print(f"Error making proxy PATCH request: {e}")

# Make a DELETE request
try:
    proxy.delete("/users/123")
    print(f"Deleted user via proxy")
except Exception as e:
    print(f"Error making proxy DELETE request: {e}")

# ============================================================================
# Using the Unify API
# ============================================================================

# Create a unify client for a specific connection
unify = client.unify("connection-id")

# Get unified chat channels
try:
    channels_response = unify.chat.channels({
        "limit": 50,
        "include_raw": True
    })
    channels = channels_response["data"]
    print(f"Found {len(channels)} chat channels")
    
    if channels_response.get("metadata", {}).get("has_more"):
        print("More channels available")
except Exception as e:
    print(f"Error getting chat channels: {e}")

# Get unified git repositories
try:
    repos_response = unify.git.repos({"limit": 25})
    repos = repos_response["data"]
    print(f"Found {len(repos)} repositories")
except Exception as e:
    print(f"Error getting repositories: {e}")

# Get unified pull requests
try:
    pulls_response = unify.git.pulls()
    pulls = pulls_response["data"]
    print(f"Found {len(pulls)} pull requests")
except Exception as e:
    print(f"Error getting pull requests: {e}")

# Get unified git tags
try:
    tags_response = unify.git.tags()
    tags = tags_response["data"]
    print(f"Found {len(tags)} tags")
except Exception as e:
    print(f"Error getting tags: {e}")

# Get unified releases
try:
    releases_response = unify.git.releases()
    releases = releases_response["data"]
    print(f"Found {len(releases)} releases")
except Exception as e:
    print(f"Error getting releases: {e}")

# Get unified project management issues
try:
    issues_response = unify.pm.issues({
        "limit": 100,
        "after": "cursor-id"
    })
    issues = issues_response["data"]
    print(f"Found {len(issues)} issues")
except Exception as e:
    print(f"Error getting issues: {e}")
