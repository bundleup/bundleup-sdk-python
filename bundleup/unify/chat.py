from typing import Any, Dict, Optional, cast
from urllib.parse import quote

from .base import Base
from .types import (
    ChannelsResponse,
    MessageResponse,
    MessagesResponse,
    UsersResponse,
)


class Chat(Base):
    def users(self, params: Optional[Dict[str, Any]] = None) -> UsersResponse:
        """
        List chat users
        """
        url = self._build_url("chat/users")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch chat/users: {response.status_code}")

        return cast(UsersResponse, response.json())

    def channels(self, params: Optional[Dict[str, Any]] = None) -> ChannelsResponse:
        """
        List chat channels
        """
        url = self._build_url("chat/channels")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch chat/channels: {response.status_code}")

        return cast(ChannelsResponse, response.json())

    def messages(
        self, channel_id: str, params: Optional[Dict[str, Any]] = None
    ) -> MessagesResponse:
        """
        List messages in a chat channel

        Newest first. ``author.name`` is None on Slack, which returns only a
        user id on a message.
        """
        if not channel_id:
            raise ValueError("channel_id is required to fetch messages.")

        endpoint = f"chat/channels/{quote(channel_id, safe='')}/messages"
        url = self._build_url(endpoint)
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(MessagesResponse, response.json())

    def message(self, channel_id: str, text: str) -> MessageResponse:
        """
        Send a chat message to a channel
        """
        if not channel_id:
            raise ValueError("channel_id is required to send a message.")

        url = self._build_url(f"chat/channels/{quote(channel_id, safe='')}/message")
        response = self._connection.post(url, json={"text": text})

        if not response.ok:
            endpoint = f"chat/channels/{quote(channel_id, safe='')}/message"
            raise Exception(f"Failed to post {endpoint}: {response.status_code}")

        return cast(MessageResponse, response.json())
