from pydantic import BaseModel

class PredictionResult(BaseModel):
    focus_status: str
    person_status: str
