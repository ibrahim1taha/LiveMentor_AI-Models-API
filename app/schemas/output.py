from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class PredictionResult(BaseModel):
    is_focus: Optional[bool] = None
    is_person: Optional[bool] = None
    is_have_thing: Optional[bool] = None
    is_sleep: Optional[bool] = None
    successful_models: List[str] = []
    failed_models: List[str] = []
    error: bool = False
    message: Optional[str] = None
