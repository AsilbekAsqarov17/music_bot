import os
import asyncio
from aiogram import Router, F, types
from aiogram.types import FSInputFile

from bot.services.search_engine import search_youtube_tracks
from bot.services.downloader import download_track_mp3
from bot.keyboards.song_keyboards import get_track_choice_keyboard

router = Router()


@router.message(F.text & ~F.text.startswith("/"))
async def handle_text_search(message: types.Message):
    query = message.text.strip()
    status_msg = await message.answer("🔍 Searching tracks...")

    loop = asyncio.get_running_loop()
    results = await loop.run_in_executor(None, search_youtube_tracks, query, 10)

    if not results:
        await status_msg.edit_text("❌ No results found. Try another query!")
        return

    response_text = f"🔎 **Top Results for:** *{query}*\n\n"
    for idx, track in enumerate(results, start=1):
        response_text += f"**{idx}.** {track['title']}\n"

    keyboard = get_track_choice_keyboard(results)
    await status_msg.edit_text(response_text, reply_markup=keyboard, parse_mode="Markdown")


@router.callback_query(F.data.startswith("dl:"))
async def handle_download_callback(callback: types.CallbackQuery):
    video_id = callback.data.split(":")[1]
    await callback.answer("⏳ Starting download...")

    status_msg = await callback.message.answer("📥 Downloading MP3, please wait...")

    mp3_file = await download_track_mp3(video_id)

    if not mp3_file or not os.path.exists(mp3_file):
        await status_msg.edit_text("❌ Download failed or file not found.")
        return

    try:
        audio = FSInputFile(mp3_file)
        await callback.message.answer_audio(
            audio=audio,
            caption="🎶 Here is your track!"
        )
        await status_msg.delete()
    except Exception as e:
        print(f"Error sending audio: {e}")
        await status_msg.edit_text("❌ Failed to send audio file.")
    finally:
        if mp3_file and os.path.exists(mp3_file):
            try:
                os.remove(mp3_file)
            except OSError as e:
                print(f"Error removing temp file: {e}")