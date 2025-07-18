from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

router = APIRouter(prefix="/ws", tags=["websocket"])

@router.websocket("/test")
async def websocket_test(websocket: WebSocket):
    await websocket.accept() 

    try:
        while True:
            data = await websocket.receive_text()

            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
 