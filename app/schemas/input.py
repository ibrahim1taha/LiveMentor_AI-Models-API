from pydantic import BaseModel

class SendFrameInput(BaseModel):
    user_id: str  
    session_id: str  
