from pydantic import BaseModel

class ImageInput(BaseModel):
    image_base64: str  # Base64-encoded frame
