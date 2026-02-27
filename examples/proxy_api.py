import os

from bundleup import BundleUp

api_key = os.getenv("BUNDLEUP_API_KEY")
connection_id = os.getenv("BUNDLEUP_CONNECTION_ID")
path = os.getenv("BUNDLEUP_PROXY_PATH", "/users")

if not api_key:
    raise SystemExit("BUNDLEUP_API_KEY is required")

if not connection_id:
    raise SystemExit("BUNDLEUP_CONNECTION_ID is required for proxy example")

client = BundleUp(api_key)
proxy = client.proxy(connection_id)

print(f"Proxy GET {path}")

try:
    response = proxy.get(path)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
except Exception as error:
    print(f"Proxy request failed: {error}")
