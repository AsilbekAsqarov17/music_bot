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

    # 1. Extract the full track name directly from the message text
    track_title = "Audio Track"
    if callback.message and callback.message.text:
        # Find which number button was clicked (e.g. "dl:1" or index matching)
        # Assuming callback.data format is "dl:video_id"
        # We can extract the title line from the message body:
        lines = callback.message.text.split("\n")

        # Look for the line corresponding to the clicked track
        # If your keyboard button stores index or if we match by search list:
        for row in callback.message.reply_markup.inline_keyboard:
            for button in row:
                if button.callback_data == callback.data:
                    btn_number = button.text.replace("🎵", "").strip()
                    for line in lines:
                        if line.startswith(f"{btn_number}."):
                            # Remove the number prefix (e.g., "1. ")
                            track_title = line.split(".", 1)[1].strip()
                            break

    status_msg = await callback.message.answer("📥 Downloading MP3, please wait...")

    mp3_file = await download_track_mp3(video_id)

    if not mp3_file or not os.path.exists(mp3_file):
        await status_msg.edit_text("❌ Download failed or file not found.")
        return

    try:
        # Clean title for filesystem safety (removes invalid characters for Windows)
        safe_filename = "".join(c for c in track_title if c.isalnum() or c in (" ", "-", "_", "(", ")", "\"")).strip()

        # Separate artist and title if '-' exists (e.g., "ARTIK & ASTI - Последний поцелуй...")
        performer = "Music Bot"
        title = track_title
        if " - " in track_title:
            parts = track_title.split(" - ", 1)
            performer = parts[0].strip()
            title = parts[1].strip()

        audio = FSInputFile(path=mp3_file, filename=f"{safe_filename}.mp3")

        await callback.message.answer_audio(
            audio=audio,
            title=title,
            performer=performer,
            caption=f"🎶 **{track_title}**",
            parse_mode="Markdown"
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