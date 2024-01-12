from aiogram.types import InlineKeyboardMarkup as ikm
from aiogram.types import InlineKeyboardButton as btn
from aiogram.utils.keyboard import InlineKeyboardBuilder as ikbuilder
from internal.content import horoscopes, horoscopes_pretty, cities, notify_timers
from internal.utils import notify_is_enable

horoscope = {}

def settings():
    btn_horoscope = btn(text="☮️ Гороскоп", callback_data="settings_horoscope")
    btn_sity = btn(text="🏘 Мой город", callback_data="settings_city")
    btn_notify = btn(text="📨 Уведомления", callback_data="settings_notify")
    k = ikm(inline_keyboard=[[
        btn_horoscope, btn_sity, btn_notify
    ]])
    return k

def settings_horoscope(user_horoscope):
    builder = ikbuilder()
    for text, call in zip(horoscopes_pretty, horoscopes, strict=True):
        smile = " ✅" if user_horoscope == call else ""
        builder.button(text=f"{text}{smile}", callback_data=f"settings_horoscope_{call}")
    builder.adjust(3, 3)
    builder.row(btn(text="↩️ Вернуться", callback_data=f"settings_back"))
    return builder.as_markup()

def settings_city(user_city: str):
    builder = ikbuilder()
    for key, city in cities.items():
        smile = "✅ " if user_city == key else ""
        builder.button(text=f'{smile}{city.get("ru")}', callback_data=f"settings_city_{key}")
    builder.adjust(2, 2)
    builder.row(btn(text="↩️ Вернуться", callback_data=f"settings_back"))
    return builder.as_markup()

def settings_notify(user_notify: int):
    builder = ikbuilder()
    for key, time in notify_timers.items():
        smile = "🚫"
        switch = "enable"
        if notify_is_enable(user_time=user_notify, time_str=time.get('en')): 
            smile = "✅"
            switch = "disable"
        builder.row(btn(text=f"{smile} {time.get('ru')}", callback_data=f"settings_notify_{key}_{switch}"))
    builder.adjust(1)   
    builder.row(btn(text="↩️ Вернуться", callback_data=f"settings_back"))
    return builder.as_markup()

