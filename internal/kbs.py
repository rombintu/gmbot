from telebot.types import InlineKeyboardMarkup as ikm
from telebot.types import InlineKeyboardButton as ikb
from content import horoscopes, horoscopes_pretty

horoscope = {}

def settings():
    k = ikm()
    k.add(ikb(text="Гороскоп", callback_data="settings_horoscope"))
    return k

def settings_horoscope():
    k = ikm(row_width=3)
    for text, call in zip(horoscopes_pretty, horoscopes, strict=True):
        k.row(ikb(text=text, callback_data=f"settings_horoscope_{call}"))
    return k