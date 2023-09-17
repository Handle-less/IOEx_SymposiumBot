import datetime

from aiogram import Bot
from aiogram.types import ParseMode

from bot.markups.keyboards.user.markups_utils import keyboard_check_visit
from bot.messages.user.messages_utils import message_remind_meeting, message_check_visit, message_announce_visit
from configuration import config
from database.models.users import Users

bot = Bot(token=config["BOT_TOKEN"], parse_mode=ParseMode.HTML)


async def reg_user(tg_id: int, tg_username: str, tg_fullname: str):
    await Users.create(
        tg_id=tg_id,
        tg_username=tg_username,
        tg_fullname=tg_fullname
    )


async def remind_meeting(sun_or_frid):
    last_run = (datetime.datetime.strptime(config['last_run'], '%d.%m.%Y')).date()
    if sun_or_frid == 'frid':
        now_date = datetime.datetime.now().date() + datetime.timedelta(days=2)
    else:
        now_date = datetime.datetime.now().date()

    if (last_run - now_date).days / 7 % 2 == 0:
        await bot.send_message(
            chat_id=config['CHAT_ID']['CHAT'],
            text=message_remind_meeting.format(
                now_date.strftime("%B"),
                now_date.day,
                now_date.year,
                config['time_meeting']
            ),
        )


async def check_visit():
    last_run = (datetime.datetime.strptime(config['last_run'], '%d.%m.%Y')).date()
    now_date = datetime.datetime.now().date()

    users = await Users.filter(role__gte=1)

    for user in users:
        user.visited = user.role
        user.role = 0
        await user.save()

    if (last_run - now_date).days / 7 % 2 == 0:
        await bot.send_message(
            chat_id=config['CHAT_ID']['ADMIN'],
            text=message_check_visit,
            reply_markup=await keyboard_check_visit()
        )


async def announce_visit():
    last_run = (datetime.datetime.strptime(config['last_run'], '%d.%m.%Y')).date()
    now_date = datetime.datetime.now().date() + datetime.timedelta(days=3)

    if (last_run - now_date).days / 7 % 2 != 0:
        await bot.send_message(
            chat_id=config['CHAT_ID']['CHAT'],
            text=message_announce_visit.format(
                now_date + datetime.timedelta(days=7),
                config['time_meeting']
            )
        )
