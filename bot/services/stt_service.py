import asyncio
from faster_whisper import WhisperModel

# Load the lightweight model once at startup (tiny or base)
# "tiny" is super fast; "base" is slightly more accurate.
model = WhisperModel("tiny", device="cpu", compute_type="int8")

def _transcribe_sync(file_path: str) -> str | None:
    """Converts voice audio file into text using Whisper."""
    try:
        segments, _ = model.transcribe(file_path, beam_size=5)
        text = " ".join([segment.text for segment in segments]).strip()
        return text if text else None
    except Exception as e:
        print(f"Speech-to-text error: {e}")
        return None

async def voice_to_text(file_path: str) -> str | None:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _transcribe_sync, file_path)