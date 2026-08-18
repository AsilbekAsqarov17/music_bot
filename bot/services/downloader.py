import os
import asyncio
from yt_dlp import YoutubeDL


async def download_track_mp3(url_or_id: str, output_dir: str = "downloads") -> str | None:
    os.makedirs(output_dir, exist_ok=True)

    target_url = url_or_id if url_or_id.startswith(("http://", "https://")) else f"https://www.youtube.com/watch?v={url_or_id}"
    out_tmpl = os.path.join(output_dir, '%(id)s.%(ext)s')

    ydl_opts = {
        # 1. Prefer m4a/opus direct audio formats to avoid heavy re-encoding
        'format': 'ba[ext=m4a]/ba/best',
        'outtmpl': out_tmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',  # 2. Lower bitrate to 128kbps (faster ffmpeg convert & smaller file size)
        }],
        # 3. Disable unnecessary metadata & playlist fetching speed bottlenecks
        'noplaylist': True,
        'concurrent_fragment_downloads': 10,  # Parallel download streams
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'mweb'],
                'player_skip': ['webpage', 'configs'],
            }
        }
    }

    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = "cookies.txt"

    def _download():
        with YoutubeDL(ydl_opts) as ydl:
            # download=True returns info dict directly without secondary API calls
            info = ydl.extract_info(target_url, download=True)
            if not info:
                return None
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            return f"{base}.mp3"

    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _download)
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None