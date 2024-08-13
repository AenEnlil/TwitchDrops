import os

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from requests import get, post
from json import dumps

from utils import form_response_message, process_subscribe_games_data
from keyboard import menu
from text import greet, menu_text, help_text, error_text, subscribed_successfully_text, \
    no_campaigns_for_subscribed_games_text, game_response_template

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    result = post(f"http://{os.getenv('hostname')}/users/", data=dumps({'user_id': msg.from_user.id}))
    await msg.answer(greet.format(name=msg.from_user.full_name), reply_markup=menu)


@router.message(Command("menu"))
async def get_menu(msg: Message):
    await msg.answer(menu_text, reply_markup=menu)


@router.message(Command("subscribe"))
async def game_subscribe(msg: Message, command: CommandObject):
    user_id = msg.from_user.id
    games = command.args
    if not games:
        return await msg.answer(error_text.format(error='game not entered'), reply_markup=menu)

    data = process_subscribe_games_data(games)
    result = post(f"http://{os.getenv('hostname')}/users/{user_id}/subscribe_to_games",
                  data=dumps({'games': data}))
    if result.status_code == 200:
        answer_text = subscribed_successfully_text.format(games=games)
        await msg.answer(answer_text, reply_markup=menu)
    else:
        await msg.answer(error_text, reply_markup=menu)


@router.callback_query(F.data == "get_all_campaigns")
async def get_all_drop_campaigns(callback: CallbackQuery):
    result = get(f"http://{os.getenv('hostname')}/campaigns/all").json()
    messages = form_response_message(result, game_response_template)
    bot = callback.bot
    chat_id = callback.message.chat.id

    try:
        for message in messages:
            await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
    except TelegramBadRequest as e:
        await bot.send_message(chat_id=chat_id, text=f'Error: {e.message}', reply_markup=menu)
    await callback.answer()


@router.callback_query(F.data == "get_subscribed_games_campaigns")
async def filter_drop_campaigns_by_subscribed_games(callback: CallbackQuery):
    bot = callback.bot
    chat_id = callback.message.chat.id
    user_id = callback.from_user.id
    result = get(f"http://{os.getenv('hostname')}/campaigns/subscribed?user_id={user_id}")
    json = result.json()

    if result.status_code == 400:
        await bot.send_message(chat_id=chat_id, text=f"Error: {result.json().get('detail')}", reply_markup=menu)
        return await callback.answer()
    elif not json:
        await bot.send_message(chat_id=chat_id, text=no_campaigns_for_subscribed_games_text, reply_markup=menu)
        return await callback.answer()

    messages = form_response_message(json, game_response_template)

    try:
        for message in messages:
            await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
    except TelegramBadRequest as e:
        await bot.send_message(chat_id=chat_id, text=f'Error: {e.message}', reply_markup=menu)
    await callback.answer()


@router.callback_query(F.data == "help")
async def get_help(callback: CallbackQuery):
    bot = callback.bot
    chat_id = callback.message.chat.id
    await bot.send_message(chat_id=chat_id, text=help_text, parse_mode=ParseMode.HTML)
    await callback.answer()
