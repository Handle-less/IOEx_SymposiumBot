from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminState(StatesGroup):
    discounts_name = State()
    discounts_sale = State()
    discounts_count = State()
    discounts_url = State()
    preset_name = State()
    presets_file = State()
    shop_file = State()
    shop_name = State()
    shop_about = State()
    shop_price = State()
    shop_add = State()
    user_data = State()
    user_balance = State()
    news_text = State()
    news_media = State()
    faq_name = State()
    faq_link = State()
    faq_change = State()
