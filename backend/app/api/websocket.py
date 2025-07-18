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
 
@router.websocket("/voice")
async def websocket_voice(websocket: WebSocket):
    await websocket.accept()
    print("Voice WebSocket connected!")

    try:
        audio_data = await websocket.receive_bytes()
        print(f"Received audion chunk: {len(audio_data)} bytes")

        await websocket.send_json({
            "type": "audio_received",
            "size": len(audio_data)
        })
    except WebSocketDisconnect:
        print("Voice client disconnected")