import asyncio
from asyncio import create_task

from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.utils import executor
from aioschedule import every, run_pending
from bot.handlers.handler_commands import register_handlers_commands
from bot.handlers.user import register_user_handlers
from bot.utils import bot, check_visit, remind_meeting

import database


async def on_startup(_):
    await database.init_database()

    create_task(scheduler())
    await bot.set_my_commands(
        [
            BotCommand("start", "Start bot"),
            BotCommand("roles", "Roles overview"),
            BotCommand("top", "Top List")
        ]
    )


async def scheduler():
    every().week.sunday.at('17:00').do(check_visit)
    every().week.sunday.at('15:00').do(remind_meeting, 'sun')
    every().week.friday.at('13:05').do(remind_meeting, 'frid')
    while True:
        await run_pending()
        await asyncio.sleep(1)


def main():
    dispatcher: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
    register_handlers_commands(dp=dispatcher)
    register_user_handlers(dp=dispatcher)

    executor.start_polling(
        dispatcher,
        skip_updates=True,
        on_startup=on_startup
    )
