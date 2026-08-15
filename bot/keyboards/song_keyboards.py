from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_track_choice_keyboard(results: list[dict]) -> InlineKeyboardMarkup:
    """
    Generates inline keyboard grid (1 to N) for search results.
    """
    buttons = []
    row = []

    for idx, track in enumerate(results, start=1):
        btn = InlineKeyboardButton(
            text=f"🎵 {idx}",
            callback_data=f"dl:{track['id']}"
        )
        row.append(btn)

        if len(row) == 5:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)