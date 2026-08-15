import os
import asyncio
from yt_dlp import YoutubeDL


async def download_track_mp3(url_or_id: str, output_dir: str = "downloads") -> str | None:
    os.makedirs(output_dir, exist_ok=True)

    target_url = url_or_id if url_or_id.startswith(("http://", "https://")) else f"https://www.youtube.com/watch?v={url_or_id}"
    out_tmpl = os.path.join(output_dir, '%(id)s.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': out_tmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['mweb', 'android', 'ios'],
            }
        },
    }

    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = "cookies.txt"

    def _download():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            return f"{base}.mp3"

    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _download)
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None