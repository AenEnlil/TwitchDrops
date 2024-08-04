from aiogram import Router, F
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from requests import get, post

from json import dumps

from utils import form_response_message
from keyboard import menu
from text import greet, menu_text, help_text

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    result = post("http://127.0.0.1:8000/users/", data=dumps({'user_id': msg.from_user.id}))
    await msg.answer(greet.format(name=msg.from_user.full_name), reply_markup=menu)


@router.message(Command("menu"))
async def get_menu(msg: Message):
    await msg.answer(menu_text, reply_markup=menu)


@router.callback_query(F.data == "get_all_campaigns")
async def get_all_drop_campaigns(callback: CallbackQuery):
    result = get("http://127.0.0.1:8000/campaigns/all").json()
    messages = form_response_message(result)
    bot = callback.bot
    chat_id = callback.message.chat.id

    try:
        for message in messages:
            await bot.send_message(chat_id=chat_id, text=message)
    except TelegramBadRequest as e:
        await bot.send_message(chat_id=chat_id, text=f'Error: {e.message}', reply_markup=menu)


@router.callback_query(F.data == "get_subscribed_games_campaigns")
async def filter_drop_campaigns_by_subscribed_games(callback: CallbackQuery):
    print(2)
    pass


@router.callback_query(F.data == "help")
async def get_help(callback: CallbackQuery):
    bot = callback.bot
    chat_id = callback.message.chat.id
    await bot.send_message(chat_id=chat_id, text=help_text)
