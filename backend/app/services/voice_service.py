import speech_recognition as sr
from gtts import gTTS
import io
from pydub import AudioSegment



class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    async def speech_to_text(self, audio_bytes: bytes, format: str = "webm") -> str:
        try:
            # Convert from WebM (or other format) to WAV
            audio = AudioSegment.from_file(
                io.BytesIO(audio_bytes), 
                format=format  # Use the format parameter!
            )
            
            # Convert to WAV in memory
            wav_buffer = io.BytesIO()
            audio.export(wav_buffer, format="wav")
            wav_buffer.seek(0)
            
            # NOW use speech recognition on the WAV
            with sr.AudioFile(wav_buffer) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
                
            print(f"Recognized: {text}")
            return text
            
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that"
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return ""  # Return empty string, not error message
        
    async def text_to_speech(self, text: str) ->bytes:
        try:
            tts = gTTS(text=text, lang='en',slow=False)

            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)

            audio_buffer.seek(0)
            return audio_buffer.read()
        except Exception as e:
            print(f"TTS error: {e}")
            return b''
        
voice_service = VoiceService()