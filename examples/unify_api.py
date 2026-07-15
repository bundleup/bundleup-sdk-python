import os

from bundleup import BundleUp

api_key = os.getenv("BUNDLEUP_API_KEY")
connection_id = os.getenv("BUNDLEUP_CONNECTION_ID")

if not api_key:
    raise SystemExit("BUNDLEUP_API_KEY is required")

if not connection_id:
    raise SystemExit("BUNDLEUP_CONNECTION_ID is required for unify example")

client = BundleUp(api_key)
unify = client.unify(connection_id)

print("Unify API example")

try:
    channels = unify.chat.channels({"limit": 10})
    print(f"Chat channels: {len(channels.get('data', []))}")
except Exception as error:
    print(f"Failed to fetch chat channels: {error}")

try:
    repos = unify.git.repos({"limit": 10})
    print(f"Git repos: {len(repos.get('data', []))}")
except Exception as error:
    print(f"Failed to fetch git repos: {error}")

try:
    tickets = unify.ticketing.tickets({"limit": 10})
    print(f"Ticketing tickets: {len(tickets.get('data', []))}")
except Exception as error:
    print(f"Failed to fetch tickets: {error}")
