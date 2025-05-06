from app.services.prediction_service import predict_from_image

# Socket.IO event handlers
def socket_events(sio):
	@sio.event
	async def connect(sid, environ):
		print("Client connected:", sid)


	#receive image data from the client
	@sio.on('send_image')
	async def handle_image(image , sessionId , userId):
		await image.read()
		result = predict_from_image(image)
		sio.emit('img_res' , {
			result , sessionId , userId
		})
		
	@sio.event
	async def disconnect(sid):
		print("Client disconnected:", sid)