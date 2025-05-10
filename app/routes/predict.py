from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import base64


from app.schemas.output import PredictionResult
from app.services.prediction_service import predict_from_image

from app.socket.socketConfig import get_socket

sio = get_socket() 

router = APIRouter()

@router.post("/predict", response_model=PredictionResult)
async def predict(image: UploadFile = File(...)):
    image_bytes = await image.read()
    # image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    result = predict_from_image(image_bytes)
    print(f"sio-----------------: {sio}")
    await sio.emit('img_res' , result) 
    print(f"Prediction result: {result}")
    return JSONResponse(content=result)