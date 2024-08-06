from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu_data = [
    [InlineKeyboardButton(text="All campaigns", callback_data="get_all_campaigns"),
     InlineKeyboardButton(text="Subscribed games campaigns", callback_data="get_subscribed_games_campaigns")],
    [InlineKeyboardButton(text="🔎 Help", callback_data="help")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu_data)
