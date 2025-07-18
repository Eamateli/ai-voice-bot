from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.voice_service import voice_service
from app.services.cohere_service import chat_with_ai
from app.services.vector_service import vector_service
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
    """Handle real-time voice conversations"""
    await websocket.accept()
    print("Voice WebSocket connected!")
    
    try:
        while True:
            # 1. Receive audio from browser
            message = await websocket.receive_text()
            data = json.loads(message)
            
            if data["type"] == "audio":
                # 2. Convert speech to text
                audio_bytes = bytes(data["audio"])  # Convert from list
                user_text = await voice_service.speech_to_text(audio_bytes)
                
                # 3. Send transcription back
                await websocket.send_json({
                    "type": "transcription",
                    "text": user_text
                })
                
                # 4. Get AI response (using your existing chat logic!)
                relevant_docs = await vector_service.search(user_text)
                context = "\n\n".join(relevant_docs) if relevant_docs else None
                ai_response, tokens = chat_with_ai(user_text, context)
                
                # 5. Convert response to speech
                audio_response = await voice_service.text_to_speech(ai_response)
                
                # 6. Send audio back
                await websocket.send_json({
                    "type": "audio_response",
                    "audio": list(audio_response),  # Convert bytes to list for JSON
                    "text": ai_response
                })
                
    except WebSocketDisconnect:
        print("Voice client disconnected") 