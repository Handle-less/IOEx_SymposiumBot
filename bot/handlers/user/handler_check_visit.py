from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from bot.markups.keyboards.user.markups_utils import keyboard_check_visit
from configuration import config
from database.models.users import Users


async def handler_check_visit(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    data = callback.data.split('_')
    user = await Users.get(
        tg_id=int(data[4])
    )
    if data[3] == '+':
        points = config[str(user.role)]['points']
        user.rank += points
    elif data[3] == 'bonus':
        points = config['roles'][str(user.role)]['points']
        user.rank += points + 2
    else:
        user.rank -= 1
    user.role = 0
    await user.save()

    await callback.message.edit_reply_markup(
        reply_markup=await keyboard_check_visit()
    )


def register_handlers_check_visits(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(handler_check_visit,
                                       text_startswith='handler_user_visit_')
