from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class ConversationBase(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=50)
    role: MessageRole
    content: str = Field(..., min_length=1)

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    role: MessageRole
    content: str

class ChatHistory(BaseModel):
    messages: list[ChatMessage]