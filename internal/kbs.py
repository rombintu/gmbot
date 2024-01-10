from aiogram.types import InlineKeyboardMarkup as ikm
from aiogram.types import InlineKeyboardButton as btn
from aiogram.utils.keyboard import InlineKeyboardBuilder as ikbuilder
from content import horoscopes, horoscopes_pretty, cities

horoscope = {}

def settings():
    btn_horoscope = btn(text="Гороскоп", callback_data="settings_horoscope")
    btn_sity = btn(text="Мой город", callback_data="settings_city")
    k = ikm(inline_keyboard=[[
        btn_horoscope, btn_sity
    ]])
    return k

def settings_horoscope():
    builder = ikbuilder()
    for text, call in zip(horoscopes_pretty, horoscopes, strict=True):
        builder.button(text=text, callback_data=f"settings_horoscope_{call}")
    builder.adjust(3, 3)
    return builder.as_markup()

def settings_city():
    builder = ikbuilder()
    for key, city in cities.items():
        builder.button(text=city.get("ru"), callback_data=f"settings_city_{key}")
    builder.adjust(2, 2)   
    return builder.as_markup()

