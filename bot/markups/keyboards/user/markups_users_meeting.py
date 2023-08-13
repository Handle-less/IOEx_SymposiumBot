from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.markups.keyboard_texts.user.keyboard_texts_users_meeting import buttons_text_keyboard_users_meeting


async def keyboard_users_meeting():
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        *[
            InlineKeyboardButton(
                text=buttons_text_keyboard_users_meeting[0],
                callback_data='handler_users_meeting'
            ),
            InlineKeyboardButton(
                text=buttons_text_keyboard_users_meeting[1],
                callback_data='handler_start'
            )
        ]
    )
    return keyboard
