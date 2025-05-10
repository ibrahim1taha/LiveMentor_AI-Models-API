from app.services.prediction_service import predict_from_image

from app.schemas.input import SendFrameInput

def socket_events(sio):
	@sio.event
	async def connect(sid, environ):
		print("Client connected:", sid)

	@sio.on('join_meeting')
	async def handle_join_meeting(sid , data):
		dataModel = SendFrameInput(**data)
		await sio.enter_room(sid, data["session_id"])
		print(f"User {dataModel.user_id} joined meeting {dataModel.session_id}")


	# handle the image data sent from the client and process it using the AI models
	@sio.on('send_image')
	async def handle_image(sid , arrBuffer , data): # separate ArrBuffer to be raw binary data == faster than wrapping it in json and base64 encoding
		dataModel = SendFrameInput(**data)

		result = predict_from_image(arrBuffer)

		print(f"Prediction result: {result}")
		
		if(result["focus_status"] != "Focused" or result["person_status"] != "OK"):
			await sio.emit('img_res' , {"userId" : dataModel.user_id , "sessionId" : dataModel.session_id , "Prediction_result": result, "sid": sid}
				, to = dataModel.session_id)
		
	
	@sio.event
	async def disconnect(sid):
		print("Client disconnected:", sid)