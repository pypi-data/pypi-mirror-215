from enum import Enum
from typing import Optional
from pydantic import BaseModel


class ApiRequestPayload(BaseModel):
    recipient: dict
    messaging_type: str = "Response"
    message:Optional[str]
