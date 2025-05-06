from fastapi import FastAPI
import socketio
from starlette.middleware.cors import CORSMiddleware
from app.routes.predict import router as predict_router
from app.socket.socketConfig import init_socket
from app.socket.socketsHandler import socket_events
# Create the Socket.IO ASGI server

sio = init_socket()
# Create FastAPI app
app = FastAPI(title="AI Focus API") 

# Add CORS middleware to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Focus Detection API"}


socket_events(sio)

# Combine FastAPI with Socket.IO as one ASGI app
app = socketio.ASGIApp(sio, other_asgi_app=app)
