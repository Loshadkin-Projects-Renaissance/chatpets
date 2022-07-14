import random
import traceback
from constants import *
from config import *
from db import Database
from telebot import types, TeleBot
import threading
import time
from datetime import date


class ReBot(TeleBot):
    def form_html_userlink(self, name, user_id):
        return f'<a href="tg://user?id={user_id}">{name}</a>'

    def respond_to(self, message, text, **kwargs):
        return self.send_message(message.chat.id, text, **kwargs)


bot = ReBot(token)
db = Database(mongo_url)

def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text, reply_markup=reply_markup,
                                 parse_mode=parse_mode)