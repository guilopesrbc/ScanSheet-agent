from typing import Dict, Any

from pydantic import BaseModel


class AIMessageModel(BaseModel):
    """Agent Message Model"""

    title: str
    content: Dict[str, Any]
