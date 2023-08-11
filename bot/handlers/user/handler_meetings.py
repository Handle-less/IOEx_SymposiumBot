import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from bot.markups.keyboards.user.markups_utils import keyboard_announce_meeting
from bot.messages.user.messages_meetings import message_role_is_full, \
    message_visit_meeting, message_closed_meeting, message_already_visit, message_not_visit, message_canceled_visit
from bot.messages.user.messages_utils import message_announce_meeting
from bot.utils import reg_user
from configuration import config

from database.models.users import Users


async def handler_visit(callback: CallbackQuery, state: FSMContext):
    await state.finish()

    user = await Users.get(
        tg_id=callback.from_user.id
    )
    user.tg_username = callback.from_user.username
    user.tg_fullname = callback.from_user.full_name
    await user.save()

    await callback.message.edit_text(
        text=message_announce_meeting,
        reply_markup=await keyboard_announce_meeting(),
    )


async def handler_meetings_visit_role(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    data = callback.data.split('_')

    user = await Users.get_or_none(
        tg_id=callback.from_user.id
    )

    if user:
        user.tg_username = callback.from_user.username
        user.tg_fullname = callback.from_user.full_name
        await user.save()
        selected_role = int(data[3])
        role_count = await Users.filter(
            role=selected_role
        )
        if selected_role == 0:
            if user.role != 0:
                user.role = 0
                await user.save()

                await callback.answer(
                    text=message_canceled_visit,
                    show_alert=True
                )

                await callback.message.edit_reply_markup(
                    reply_markup=await keyboard_announce_meeting()
                )
            else:
                await callback.answer(
                    text=message_not_visit,
                    show_alert=True
                )
        elif user.role == selected_role:
            await callback.answer(
                text=message_already_visit,
                show_alert=True
            )
        elif role_count == config['roles'][str(selected_role)]['max']:
            await callback.answer(
                text=message_role_is_full,
                show_alert=True
            )
        else:
            user.role = selected_role
            await user.save()
            last_run = datetime.datetime.strptime(config['last_run'], '%d.%m.%Y').date()
            last_week = last_run.weekday()
            now_date = datetime.datetime.now().date()
            now_week = now_date.weekday()

            meet_date = now_date + datetime.timedelta(days=last_week - now_week)
            if (last_run - meet_date).days / 7 % 2 != 0:
                meet_date += datetime.timedelta(days=7)
            await callback.message.answer(
                text=message_visit_meeting.format(
                    config['roles'][str(selected_role)]['name'],
                    meet_date
                )
            )
            await callback.message.edit_reply_markup(
                reply_markup=await keyboard_announce_meeting()
            )
    else:
        await reg_user(
            tg_id=callback.from_user.id,
            tg_username=callback.from_user.username,
            tg_fullname=callback.from_user.full_name
        )
        await handler_meetings_visit_role(
            callback=callback,
            state=state
        )


async def handler_close_message(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.delete()


def register_handlers_meetings(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(handler_visit,
                                       text='handler_visit')
    dp.register_callback_query_handler(handler_meetings_visit_role,
                                       text_startswith='handler_meetings_role_')
    dp.register_callback_query_handler(handler_close_message,
                                       text='handler_close_message')
