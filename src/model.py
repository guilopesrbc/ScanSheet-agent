from typing import Dict, Any

from pydantic import BaseModel


class AIMessageModel(BaseModel):
    title: str
    content: Dict[str, Any]