from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.markups.keyboards.user.markups_commands import keyboard_start_menu, keyboard_go_to_menu
from bot.markups.keyboards.user.markups_roles import keyboard_roles_list
from bot.messages.user.messages_commands import message_command_start, message_command_top
from bot.messages.user.messages_roles import message_roles_list
from bot.utils import reg_user

from database.models.users import Users


async def handler_command_start(message: Message, state: FSMContext):
    await state.finish()
    user = await Users.get_or_none(
        tg_id=message.chat.id
    )
    if user:
        user.tg_username = message.chat.username
        user.tg_fullname = message.chat.full_name
        await user.save()

        await message.answer(
            text=message_command_start.format(
                user.tg_fullname,
                user.rank
            ),
            reply_markup=await keyboard_start_menu(user_id=user.tg_id)
        )
    else:
        await reg_user(
            tg_id=message.chat.id,
            tg_username=message.chat.username,
            tg_fullname=message.chat.full_name
        )
        await handler_command_start(
            message=message,
            state=state
        )


async def handler_command_roles(message: Message, state: FSMContext):
    await state.finish()
    user = await Users.get_or_none(
        tg_id=message.chat.id
    )
    if user:
        user.tg_username = message.chat.username
        user.tg_fullname = message.chat.full_name
        await user.save()

        await message.answer(
            text=message_roles_list,
            reply_markup=await keyboard_roles_list()
        )
    else:
        await reg_user(
            tg_id=message.chat.id,
            tg_username=message.chat.username,
            tg_fullname=message.chat.full_name
        )
        await handler_command_roles(
            message=message,
            state=state
        )


async def handler_command_top(message: Message, state: FSMContext):
    await state.finish()
    user = await Users.get_or_none(
        tg_id=message.chat.id
    )
    if user:
        user.tg_username = message.chat.username
        user.tg_fullname = message.chat.full_name
        await user.save()

        users = (await Users.all().group_by(
            'rank'
        ))[:5]
        top_users = ''
        for top_user in users:
            top_users += f'{top_user.tg_fullname} - {top_user.rank}\n'

        await message.answer(
            text=message_command_top.format(
                top_users
            ),
            reply_markup=await keyboard_go_to_menu()
        )
    else:
        await reg_user(
            tg_id=message.chat.id,
            tg_username=message.chat.username,
            tg_fullname=message.chat.full_name
        )
        await handler_command_roles(
            message=message,
            state=state
        )


async def handler_top_list(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    user = await Users.get(
        tg_id=callback.from_user.id
    )
    user.tg_username = callback.from_user.username
    user.tg_fullname = callback.from_user.full_name
    await user.save()

    users = (await Users.all().group_by(
        'rank'
    ))[:5]
    top_users = ''
    for top_user in users:
        top_users += f'{top_user.tg_fullname} - {top_user.rank}\n'

    await callback.message.edit_text(
        text=message_command_top.format(
            top_users
        ),
        reply_markup=await keyboard_go_to_menu()
    )


async def handler_start(callback: CallbackQuery, state: FSMContext):
    await state.finish()

    user = await Users.get(
        tg_id=callback.from_user.id
    )
    user.tg_username = callback.from_user.username
    user.tg_fullname = callback.from_user.full_name
    await user.save()

    await callback.message.edit_text(
            text=message_command_start.format(
                user.tg_fullname,
                user.rank
            ),
            reply_markup=await keyboard_start_menu(user_id=user.tg_id)
        )


def register_handlers_commands(dp: Dispatcher) -> None:
    dp.register_message_handler(handler_command_start, commands=['start'], state='*')
    dp.register_message_handler(handler_command_roles, commands=['roles'], state='*')
    dp.register_message_handler(handler_command_top, commands=['top'], state='*')
    dp.register_callback_query_handler(handler_start, text='handler_start', state='*')
    dp.register_callback_query_handler(handler_top_list, text='command_top', state='*')
