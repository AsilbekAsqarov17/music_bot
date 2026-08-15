import os
from shazamio import Shazam

shazam = Shazam()


async def recognize_audio(file_path: str) -> dict | None:
    """
    Recognizes song title and artist from an audio/voice file using ShazamIO.
    """
    if not os.path.exists(file_path):
        return None

    out = await shazam.recognize(file_path)
    track = out.get("track")
    if not track:
        return None

    title = track.get("title", "Unknown Title")
    subtitle = track.get("subtitle", "Unknown Artist")

    return {
        "title": title,
        "artist": subtitle,
        "full_name": f"{subtitle} - {title}"
    }