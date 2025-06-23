from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    flow_keyword: Optional[str] = Field(None, description="Ongoing flow")
    question: str = Field(..., description="User's chat message")
    thread_id: Optional[str] = Field(None, description="ID of the conversation thread")
    json_extractor_thread_id: Optional[str] = Field(None, description="ID of the conversation thread")
    is_user_registered: bool = True


