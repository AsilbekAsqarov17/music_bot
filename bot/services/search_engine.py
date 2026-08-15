from yt_dlp import YoutubeDL

def search_youtube_tracks(query: str, max_results: int = 10) -> list[dict]:
    """
    Searches YouTube for tracks matching the query and returns top results.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }

    # Ensure search prefix is explicitly attached to the query string
    search_query = f"ytsearch{max_results}:{query}"

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=False)
        entries = info.get('entries', [])

    results = []
    for entry in entries:
        if not entry:
            continue
        results.append({
            'title': entry.get('title', 'Unknown Title'),
            'url': entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}",
            'duration': entry.get('duration', 0),
            'id': entry.get('id')
        })
    return results