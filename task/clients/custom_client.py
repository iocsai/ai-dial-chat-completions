import json
from random import choices

import aiohttp
import requests

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient:
    _endpoint: str
    _api_key: str

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        self._endpoint = DIAL_ENDPOINT + f"/openai/deployments/{deployment_name}/chat/completions"

    def get_completion(self, messages: list[Message]) -> Message:
        # 1. Create headers dict with api-key and Content-Type
        headers = self.get_headers()

        # 2. Create request_data dictionary with:
        request_data = {
            "messages": [msg.to_dict() for msg in messages]
        }

        # 3. Make POST request using requests.post() with:
        response = requests.post(self._endpoint, json=request_data, headers=headers)

        # 4. Get content from response, print it and return message with assistant role and content
        if response.status_code == 200:
            data = response.json()
            custom_choices = data.get("choices", [])
            if custom_choices:
                content = custom_choices[0].get("message", {}).get("content")
                print(content)
                return Message(Role.AI, content)
            raise ValueError("No Choice has been present in the response")

        # 5. If status code != 200 then raise Exception with format: f"HTTP {response.status_code}: {response.text}"
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

    async def stream_completion(self, messages: list[Message]) -> Message:
        # 1. Create headers dict with api-key and Content-Type
        headers = self.get_headers()

        # 2. Create request_data dictionary with:
        request_data = {
            "messages": [msg.to_dict() for msg in messages],
            "stream": True
        }

        # 3. Create empty list called 'contents' to store content snippets
        contents = []

        # 4. Create aiohttp.ClientSession() using 'async with' context manager
        async with aiohttp.ClientSession() as session:

            # 5. Inside session, make POST request using session.post() with:

    def get_headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "api-key": self._api_key
        }
        return headers

