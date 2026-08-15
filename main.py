import asyncio
from aiogram import Bot, Dispatcher

from bot.config import BOT_TOKEN
from bot.handlers import start_router, text_search_router, voice_recognition_router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Include all route handlers
    dp.include_router(start_router)
    dp.include_router(text_search_router)
    dp.include_router(voice_recognition_router)

    print("🚀 Bot is running and listening for updates...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())