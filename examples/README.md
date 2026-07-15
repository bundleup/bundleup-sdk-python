# BundleUp Python SDK Examples

This folder contains runnable scripts that show common SDK workflows.

## Prerequisites

- Python 3.8+
- `pip install -r requirements.txt` run from `bundleup-sdk-python/`
- `BUNDLEUP_API_KEY` set in your environment

For examples that use a connected integration, also set:

- `BUNDLEUP_CONNECTION_ID`

## Run an Example

From `bundleup-sdk-python/`:

```bash
python examples/basic_usage.py
python examples/proxy_api.py
python examples/unify_api.py
```

## Scripts

- `basic_usage.py` — initialize the SDK and list connections, integrations, and webhooks
- `proxy_api.py` — send a GET request through the Proxy API
- `unify_api.py` — call Unify Chat, Git, and Ticketing endpoints
