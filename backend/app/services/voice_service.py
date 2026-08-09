import speech_recognition as sr
from gtts import gTTS
import io
import httpx
from pydub import AudioSegment
from app.config import settings

ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech"


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

    async def text_to_speech(self, text: str) -> bytes:
        """Generate MP3 audio with ElevenLabs, falling back to gTTS on failure."""
        if not settings.ELEVENLABS_API_KEY:
            print("ELEVENLABS_API_KEY is not set, using gTTS")
            return self._gtts(text)

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{ELEVENLABS_TTS_URL}/{settings.ELEVENLABS_VOICE_ID}",
                    headers={
                        "xi-api-key": settings.ELEVENLABS_API_KEY,
                        "Content-Type": "application/json",
                    },
                    params={"output_format": "mp3_44100_128"},
                    json={
                        "text": text,
                        "model_id": settings.ELEVENLABS_MODEL_ID,
                    },
                )

            if response.status_code != 200:
                print(f"ElevenLabs TTS failed ({response.status_code}): {response.text[:300]}")
                return self._gtts(text)

            return response.content

        except Exception as e:
            print(f"ElevenLabs TTS error: {e}")
            return self._gtts(text)

    def _gtts(self, text: str) -> bytes:
        try:
            tts = gTTS(text=text, lang='en', slow=False)

            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)

            audio_buffer.seek(0)
            return audio_buffer.read()
        except Exception as e:
            print(f"TTS error: {e}")
            return b''

voice_service = VoiceService()
