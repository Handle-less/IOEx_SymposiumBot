from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    deposit_sum = State()
    account_details = State()
    proxy = State()
    parser_input = State()
    check_file = State()
    anti_public_repeat = State()
    strings_base_file = State()
    delay = State()
    preset_name = State()
    preset_text = State()
    change_preset = State()
    links_count = State()
    retweet_query = State()
    retweet_count = State()
    boost_data = State()
