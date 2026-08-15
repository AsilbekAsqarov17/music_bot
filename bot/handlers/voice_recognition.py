import os
import asyncio
from aiogram import Router, F, types

from bot.services.stt_service import voice_to_text
from bot.services.search_engine import search_youtube_tracks
from bot.keyboards.song_keyboards import get_track_choice_keyboard

router = Router()


@router.message(F.voice | F.audio)
async def handle_voice_search(message: types.Message, bot):
    status_msg = await message.answer("🗣️ Transcribing voice note to text...")

    os.makedirs("temp_audio", exist_ok=True)
    audio_obj = message.voice or message.audio
    file_info = await bot.get_file(audio_obj.file_id)

    temp_path = f"temp_audio/{audio_obj.file_id}.ogg"
    await bot.download_file(file_info.file_path, temp_path)

    try:
        # Step 1: Transcribe Voice to Text
        recognized_text = await voice_to_text(temp_path)

        if not recognized_text:
            await status_msg.edit_text("❌ Could not transcribe any spoken words. Please speak clearly!")
            return

        await status_msg.edit_text(f"🗣️ **Recognized:** *\"{recognized_text}\"*\n\n🔎 Searching YouTube...")

        # Step 2: Search YouTube using recognized text
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(None, search_youtube_tracks, recognized_text, 10)

        if not results:
            await status_msg.edit_text(f"❌ No YouTube results found for: *\"{recognized_text}\"*")
            return

        response_text = f"🔎 **Top Results for:** *\"{recognized_text}\"*\n\n"
        for idx, track in enumerate(results, start=1):
            response_text += f"**{idx}.** {track['title']}\n"

        keyboard = get_track_choice_keyboard(results)
        await status_msg.edit_text(response_text, reply_markup=keyboard, parse_mode="Markdown")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)