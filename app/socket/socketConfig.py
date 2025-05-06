import socketio
from starlette.middleware.cors import CORSMiddleware

sio = None

def init_socket():
	global sio
	if sio is None: 
		sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
	return sio

def get_socket():
    global sio
    if sio is None: 
        return init_socket()
    return sio