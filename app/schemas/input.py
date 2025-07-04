from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile

class SendFrameInput(BaseModel):
    user_id: str  
    session_id: str  

class FrameRequest(BaseModel):
    id: str
    frame: UploadFile

class BatchPredictionRequest(BaseModel):
    frames: List[FrameRequest]
