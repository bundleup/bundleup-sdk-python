import os

from bundleup import BundleUp

api_key = os.getenv("BUNDLEUP_API_KEY")

if not api_key:
    raise SystemExit("BUNDLEUP_API_KEY is required")

client = BundleUp(api_key)

print("BundleUp Python SDK: basic usage")

try:
    connections = client.connection.list()
    print(f"Connections: {len(connections)}")
except Exception as error:
    print(f"Failed to list connections: {error}")

try:
    integrations = client.integration.list()
    print(f"Integrations: {len(integrations)}")
except Exception as error:
    print(f"Failed to list integrations: {error}")

try:
    webhooks = client.webhook.list()
    print(f"Webhooks: {len(webhooks)}")
except Exception as error:
    print(f"Failed to list webhooks: {error}")
