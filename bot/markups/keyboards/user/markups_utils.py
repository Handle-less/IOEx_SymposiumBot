from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.markups.keyboard_texts.keyboard_text_roles import buttons_text_keyboard_roles_list
from bot.markups.keyboard_texts.user.keyboard_texts_utils import buttons_text_keyboard_announce_meetings, \
    buttons_text_keyboard_remind_meeting
from configuration import config
from database.models.users import Users


async def keyboard_announce_meeting():
    keyboard = InlineKeyboardMarkup(row_width=2)

    for x in range(1, 8):
        role_count = await Users.filter(
            role=x
        ).count()
        keyboard.add(
            *[
                InlineKeyboardButton(
                    text=f'{config["roles"][str(x)]["name"]} [{role_count}/{config["roles"][str(x)]["max"]}]',
                    callback_data=f'handler_meetings_role_{x}'
                ),
                InlineKeyboardButton(
                    text=buttons_text_keyboard_announce_meetings[0],
                    callback_data=f'handler_roles_see_{config["roles"][str(x)]["about"]}'
                )
            ]
        )
    keyboard.add(
        InlineKeyboardButton(
            text=buttons_text_keyboard_announce_meetings[1],
            callback_data='handler_meetings_role_0'
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=buttons_text_keyboard_roles_list[0],
            callback_data='handler_start'
        )
    )

    return keyboard


async def keyboard_check_visit():
    keyboard = InlineKeyboardMarkup(row_width=3)

    users = await Users.filter(
        role__gte=1
    )
    for user in users:
        keyboard.add(
            *[
                InlineKeyboardButton(
                    text=user.tg_fullname,
                    callback_data='_'
                ),
                InlineKeyboardButton(
                    text='➕',
                    callback_data=f'handler_user_visit_+_{user.tg_id}'
                ),
                InlineKeyboardButton(
                    text='➖',
                    callback_data=f'handler_user_visit_-_{user.tg_id}'
                )
            ]
        )

    return keyboard
