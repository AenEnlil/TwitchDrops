import os

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from dotenv import load_dotenv

from bot.text import new_campaigns_text, game_response_template
from bot.utils import form_response_message

load_dotenv()


async def notify_users_about_new_campaign(user_ids: list, campaigns: list):
    session = AiohttpSession()
    bot = Bot(token=os.getenv('bot_token'), session=session)
    for user_id in user_ids:
        messages = form_response_message(campaigns,game_response_template)

        try:
            for message in messages:
                await bot.send_message(chat_id=user_id, text=new_campaigns_text+message, parse_mode=ParseMode.HTML)
        except TelegramBadRequest as e:
            await bot.send_message(chat_id=user_id, text=f'Error: {e.message}')
