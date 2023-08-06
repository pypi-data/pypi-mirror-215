from typing import Dict, Optional
from requests import Response, post, get
from .execeptions import SendingMessageFailedException
from .types import ApiRequestPayload


class MessengerAPI:

    def __init__(self,  access_token: str, page_id: str, api_version: str = 'v16.0'):
        self.access_token = access_token
        self.base_url = f'https://graph.facebook.com/{api_version}/{page_id}'
        self.headers: Dict[str, str] = {
            'Content-Type': 'application/json',
        }

    def send_text_message(self, user_id: str, message):
        payload = ApiRequestPayload(
            recipient={"id": user_id}, message={"text": str(message)})
        url = f"{self.base_url}/messages?access_token={self.access_token}"
        result = post(url, headers=self.headers, data=payload.json())

        if result.status_code != 200:
            raise SendingMessageFailedException(result.status_code)
        return result

    def get_media(self, uri: str) -> Optional[Response]:
        response = get(uri, stream=True)
        response.raise_for_status()
        return response