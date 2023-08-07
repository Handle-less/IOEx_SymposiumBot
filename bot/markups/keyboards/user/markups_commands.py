from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.markups.keyboard_texts.user.keyboard_texts_commands import buttons_text_keyboard_start
from bot.markups.keyboard_texts.user.keyboard_texts_utils import buttons_text_keyboard_remind_meeting


async def keyboard_start_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(
            text=buttons_text_keyboard_start[0],
            callback_data='handler_visit'
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=buttons_text_keyboard_start[1],
            callback_data='command_top'
        ),
        InlineKeyboardButton(
            text=buttons_text_keyboard_start[2],
            callback_data='command_roles'
        )
    )

    return keyboard


async def keyboard_go_to_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=buttons_text_keyboard_remind_meeting[0],
            callback_data='handler_start'
        )
    )

    return keyboard
