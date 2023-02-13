import os

from store.store import Database
from telebot import TeleBot
from content import acivate_message, deactivate_message
from utils import pretty_info
from dotenv import load_dotenv
load_dotenv()

bot = TeleBot(os.getenv("TOKEN"), parse_mode=None)
store = Database(os.getenv("STORE", "sqlite:///store/db.sqlite"))


@bot.message_handler(commands=['start', 'activate'])
def handle_message_start(message):
    store.login(message.chat.id)
    bot.send_message(
        message.chat.id, 
        acivate_message
    )
    bot.send_message(
        message.chat.id, 
        pretty_info(), 
        parse_mode="markdown"
    )

@bot.message_handler(commands=['deactivate'])
def handle_message_start(message):
    store.deactivate(message.chat.id)
    bot.send_message(
        message.chat.id, 
        deactivate_message
    )

@bot.message_handler(commands=['try'])
def handle_message_start(message):
    bot.send_message(
        message.chat.id, 
        pretty_info(), 
        parse_mode="markdown"
    )

def notify():
    users = store.get_users()
    mess = pretty_info()
    for u in users:
        try:
            bot.send_message(u, mess, parse_mode="markdown")
        except Exception as err:
            pass