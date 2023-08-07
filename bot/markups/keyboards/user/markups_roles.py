from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.markups.keyboard_texts.keyboard_text_roles import buttons_text_keyboard_roles_list, \
    buttons_text_keyboard_roles_back
from bot.markups.keyboard_texts.user.keyboard_texts_utils import buttons_text_keyboard_remind_meeting
from configuration import config
from database.models.users import Users


async def keyboard_roles_list():
    keyboard = InlineKeyboardMarkup(row_width=2)

    for x in range(1, 8):
        keyboard.add(
            *[
                InlineKeyboardButton(
                    text=f'{config["roles"][str(x)]["name"]}',
                    callback_data=f'handler_roles_see_{config["roles"][str(x)]["about"]}'
                )
            ]
        )
    keyboard.add(
        InlineKeyboardButton(
            text=buttons_text_keyboard_roles_list[0],
            callback_data='handler_start'
        )
    )
    return keyboard


async def keyboard_roles_back():
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        InlineKeyboardButton(
            text=buttons_text_keyboard_roles_back[0],
            callback_data='command_roles'
        )
    )
    return keyboard
