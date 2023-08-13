from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from bot.markups.keyboards.user.markups_users_meeting import keyboard_users_meeting
from bot.messages.user.messages_users_meeting import message_users_meeting
from configuration import config
from database.models.users import Users


async def handler_users_meeting(callback: CallbackQuery, state: FSMContext):
    await state.finish()

    users = await Users.filter(
        role__gte=1
    )
    text = '\n\n'.join(f'user: {x.tg_fullname}\n'
                     f'role: {config["roles"][str(x.role)]["name"]}\n'
                     f'rate: {x.rank}' for x in users)

    await callback.message.edit_text(
        text=message_users_meeting.format(
            len(users),
            text
        ),
        reply_markup=await keyboard_users_meeting()
    )


def register_handlers_users_meeting(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(handler_users_meeting,
                                       text='handler_users_meeting')
