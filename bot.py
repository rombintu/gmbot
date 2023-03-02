import os

from store.store import Database
from telebot import TeleBot
from telebot import types
from content import acivate_message, deactivate_message
from internal import kbs
from utils import pretty_info, get_horoscopies, get_horoscope
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
def handle_message_deactivate(message):
    store.deactivate(message.chat.id)
    bot.send_message(
        message.chat.id, 
        deactivate_message
    )

@bot.message_handler(commands=['try'])
def handle_message_try(message):
    user = store.get_user(message.chat.id)
    hrs = get_horoscope(user["horoscope"])[-1]
    bot.send_message(
        message.chat.id, 
        pretty_info().format(hrs), 
        parse_mode="markdown"
    )

@bot.message_handler(commands=["settings"])
def handle_message_settings(message):
    bot.send_message(
        message.chat.id,
        "⚙️ Настройки",
        reply_markup=kbs.settings(),
    )

def notify():
    users = store.get_users()
    mess = pretty_info()
    hrs = get_horoscopies()
    for u in users:
        try:
            bot.send_message(u["uuid"], mess.format(hrs[u["horoscope"]]), parse_mode="markdown")
        except Exception as err:
            print(err)
            store.delete_user(u)

def send_all(message):
    users = store.get_users()
    for u in users:
        try:
            bot.send_message(u["uuid"], message, parse_mode="markdown")
        except Exception as err:
            print(err)

@bot.callback_query_handler(func=lambda c: c.data)
def callbacks(c: types.CallbackQuery):
    data = c.data.split("_")
    match data:
        case ["settings", "horoscope"]:
            bot.edit_message_text(
                    "Выбери свой гороскоп",
                    c.from_user.id, c.message.id,
                    reply_markup=kbs.settings_horoscope()
                )
        case ["settings", "horoscope", _]:
            target = data[-1]
            store.user_update_horoscope(c.from_user.id, target)
            bot.edit_message_text(
                    "Настройки сохранены",
                    c.from_user.id, c.message.id,
                )
