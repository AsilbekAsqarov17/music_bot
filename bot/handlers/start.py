from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        f"👋 <b>Hello, {message.from_user.first_name}!</b>\n\n"
        "Welcome to the <b>Music Search Bot</b>! 🎵\n\n"
        "Here is how you can find songs:\n"
        "• <b>Text Search:</b> Simply send me a song name or singer's name.\n"
        "• <b>Voice Search:</b> Send me a voice message/audio clip of a song.\n\n"
        "Type /help to see all available commands!"
    )
    await message.answer(welcome_text, parse_mode="HTML")


@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "🛠 <b>How to use this bot:</b>\n\n"
        "1️⃣ <b>Search by Song Name:</b> Send the title (e.g., <code>Shape of You</code>), and I will show you top results.\n"
        "2️⃣ <b>Search by Artist:</b> Send an artist's name (e.g., <code>Eminem</code>), and I will list their top tracks.\n"
        "3️⃣ <b>Voice Recognition:</b> Send a voice recording or audio clip, and I will identify the track for you!\n\n"
        "💡 <i>Just type your search query right into the chat to begin!</i>"
    )
    await message.answer(help_text, parse_mode="HTML")