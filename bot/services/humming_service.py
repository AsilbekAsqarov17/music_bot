import os
import base64
import hashlib
import hmac
import time
import asyncio
import requests
from bot.config import ACR_HOST, ACR_ACCESS_KEY, ACR_ACCESS_SECRET


def _recognize_humming_sync(file_path: str) -> dict | None:
    if not ACR_HOST or not ACR_ACCESS_KEY or not ACR_ACCESS_SECRET:
        print("ACRCloud credentials missing in environment.")
        return None

    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"
    timestamp = str(int(time.time()))

    string_to_sign = f"{http_method}\n{http_uri}\n{ACR_ACCESS_KEY}\n{data_type}\n{signature_version}\n{timestamp}"

    sign = base64.b64encode(
        hmac.new(
            ACR_ACCESS_SECRET.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha1
        ).digest()
    ).decode('utf-8')

    data = {
        'access_key': ACR_ACCESS_KEY,
        'sample_bytes': os.path.getsize(file_path),
        'timestamp': timestamp,
        'signature': sign,
        'data_type': data_type,
        'signature_version': signature_version
    }

    url = f"https://{ACR_HOST}{http_uri}"

    try:
        with open(file_path, 'rb') as f:
            files = {'sample': f}
            response = requests.post(url, data=data, files=files, timeout=10)

        res_json = response.json()
        status = res_json.get("status", {})

        if status.get("code") == 0:
            music_list = res_json.get("metadata", {}).get("music", [])
            if music_list:
                track = music_list[0]
                title = track.get("title", "Unknown Title")
                artists = [a.get("name") for a in track.get("artists", [])]
                artist_str = ", ".join(artists) if artists else "Unknown Artist"
                return {
                    "title": title,
                    "artist": artist_str,
                    "full_name": f"{artist_str} - {title}"
                }
    except Exception as e:
        print(f"ACRCloud Error: {e}")

    return None


async def recognize_humming(file_path: str) -> dict | None:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _recognize_humming_sync, file_path)