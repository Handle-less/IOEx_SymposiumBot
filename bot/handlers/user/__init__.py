from aiogram import Dispatcher

from bot.handlers.user import handler_meetings, handler_roles, handler_check_visit


def register_user_handlers(dp: Dispatcher) -> None:
    handler_meetings.register_handlers_meetings(dp)
    handler_roles.register_handlers_roles(dp)
    handler_check_visit.register_handlers_check_visits(dp)
