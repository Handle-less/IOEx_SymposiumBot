import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.markups.keyboard_texts.user.keyboard_texts_commands import buttons_text_keyboard_start
from bot.markups.keyboard_texts.user.keyboard_texts_utils import buttons_text_keyboard_remind_meeting
from configuration import config


async def keyboard_start_menu(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    last_run = datetime.datetime.strptime(config['last_run'], '%d.%m.%Y').date()
    last_week = last_run.weekday()
    now_date = datetime.datetime.now().date()
    now_week = now_date.weekday()

    meet_date = now_date + datetime.timedelta(days=last_week-now_week)
    if (last_run - meet_date).days / 7 % 2 != 0:
        meet_date += datetime.timedelta(days=7)

    keyboard.add(
        InlineKeyboardButton(
            text=buttons_text_keyboard_start[0].format(
                f'{meet_date.strftime("%B")}, {meet_date.day}'
            ),
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
    if user_id in config['ADMINS_ID']:
        keyboard.add(
            InlineKeyboardButton(
                text=buttons_text_keyboard_start[3],
                callback_data='handler_users_meeting'
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
