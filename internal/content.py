from datetime import datetime as dt

acivate_message = """Добрый день! 
Вы успешно подписаны на ежедневную рассылку сообщений в 7:00 МСК

Предложения по улучшению: @rombintu
Отписаться: /deactivate"""

deactivate_message = "Вы отписались от рассылки. Вернуть: /activate"

horoscopes = [
    "none",
    "aries", # Oven
    "taurus", # Teletc
    "gemini", # Bliznecy
    "cancer", # Rak
    "leo", # Lev
    "virgo", # Deva
    "libra", # Vesy
    "scorpio", # Scorpio
    "sagittarius", # Streletc
    "capricorn", # Kozerok
    "aquarius", # Vodoley
    "pisces", # Riby
]

horoscopes_pretty = [
    "❌ Отключить",
    "♈️ Овен",
    "♉️ Телец",
    "♊️ Близнецы",
    "♋️ Рак",
    "♌️ Лев",
    "♍️ Дева",
    "♎️ Весы",
    "♏️ Скорпион",
    "♐️ Стрелец",
    "♑️ Козерог",
    "♒️ Водолей",
    "♓️ Рыбы",
]

cities = {
    "msk": {"val": "moskva", "ru": "Москва, Россия", "plus": 0},
    "spb": {"val": "sankt-peterburg", "ru": "Санкт-Петербург, Россия", "plus": 0},
    "nvb": {"val": "novosibirsk", "ru": "Новосибирск, Россия", "plus": 3},
    "ekt": {"val": "ekaterinburg", "ru": "Екатеринбург, Россия", "plus": 2},
    "niz": {"val": "nizhniy-novgorod", "ru": "Нижний Новгород, Россия", "plus": 0},
    "smr": {"val": "samara", "ru": "Самара, Россия", "plus": 1},
    "oms": {"val": "omsk", "ru": "Омск, Россия", "plus": 3},
    "kaz": {"val": "kazan", "ru": "Казань, Россия", "plus": 0},
    "rov": {"val": "rostov-na-donu", "ru": "Ростов-на-Дону, Россия", "plus": 0},
    "chl": {"val": "chelyabinsk", "ru": "Челбинск, Россия", "plus": 2},
    "sch": {"val": "sochi", "ru": "Сочи, Россия", "plus": 0},
    "evn": {"val": "erevan", "ru": "Ереван, Армения", "plus": 1},
    "tbs": {"val": "tbilisi", "ru": "Тбилиси, Грузия", "plus": 1}
}

notify_timers = {
    1: {"val": dt.strptime("07:00", "%H:%M"), "ru": "Утром (07:00)", "en": "morning"},
    2: {"val": dt.strptime("12:00", "%H:%M"), "ru": "Днем (12:00)", "en": "daytime"},
    4: {"val": dt.strptime("18:00", "%H:%M"), "ru": "Вечером (18:00)", "en": "evening"}
}
