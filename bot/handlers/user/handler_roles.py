from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from bot.markups.keyboards.user.markups_roles import keyboard_roles_list, keyboard_roles_back
from bot.messages.user.messages_roles import message_roles_list
from database.models.users import Users


async def handler_roles_list(callback: CallbackQuery, state: FSMContext):
    await state.finish()

    user = await Users.get(
        tg_id=callback.from_user.id
    )
    user.tg_username = callback.from_user.username
    user.tg_fullname = callback.from_user.full_name
    await user.save()

    await callback.message.delete()

    await callback.message.answer(
        text=message_roles_list,
        reply_markup=await keyboard_roles_list()
    )


async def handler_roles_see(callback: CallbackQuery, state: FSMContext):
    await state.finish()

    user = await Users.get(
        tg_id=callback.from_user.id
    )
    user.tg_username = callback.from_user.username
    user.tg_fullname = callback.from_user.full_name
    await user.save()

    data = callback.data.split('_')

    await callback.message.delete()

    await callback.message.answer_photo(
        photo=open(f'roles/{data[3]}', 'rb'),
        reply_markup=await keyboard_roles_back()
    )


def register_handlers_roles(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(handler_roles_list,
                                       text='command_roles')
    dp.register_callback_query_handler(handler_roles_see,
                                       text_startswith='handler_roles_see_')
