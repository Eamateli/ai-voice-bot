import speech_recognition as sr
from gtts import gTTS
import io
from pydub import AudioSegment



class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    async def speech_to_text(self, audio_bytes: bytes) -> str:
        try:
            audio_file = io.BytesIO(audio_bytes)

            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)

            return text
        
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that"
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return "Error processing audio"
        
    async def text_to_speech(self, text: str) ->bytes:
        try:
            tts = gTTS(text=text, lang='en',slow=False)

            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)

            audio_buffer.seek(0)
            return audio_buffer.read()
        except Exception as e:
            print(f"TTS error: {e}")
            return b' '
        
voice_service = VoiceService()