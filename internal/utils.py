import requests
from datetime import datetime as dt
from datetime import timedelta
import locale
from internal.store import Database
from internal import logger
from bs4 import BeautifulSoup as BS
from internal.content import horoscopes, cities
from internal.content import notify_timers as ntv_d
from functools import cache

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

def get_finance_rub(valutes: list[str]):
    try:
        curs_dict = {}
        req = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        for valute in valutes:
            curs_dict[valute] = str(round(req['Valute'][valute]['Value'], 2))
    except Exception as err:
        print(err)
    return curs_dict

def get_finance_bitcoin():
    try:
        req: dict = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json').json()
        return int(req.get('bpi').get('USD').get('rate_float'))
    except Exception as err:
        print(err)
        return 0

def get_holiday(tomorrow=False):
    try:
        data = requests.get("https://www.calend.ru/")
        soup = BS(data.text, 'html.parser')
        all_holidays = soup.find("ul", class_="itemsNet").find_all("li", class_="one-two")
        today = all_holidays[0].find("div", class_="caption").text.strip()
        tomorrow = all_holidays[-1].find("div", class_="caption").text.strip()
        return [today, tomorrow]
    except Exception as err:
        print(err)
        return []

def get_weather_meteoservice_ru(city="msk"):
    user_city = cities.get(city)
    url = f"https://www.meteoservice.ru/weather/today/{user_city.get('val')}"
    text = ""
    try:
        data = requests.get(url)
        soup = BS(data.text, "html.parser")
        text = soup.find("strong").text
        return text + f"\n[Метеосервис.ру {user_city.get('ru')}]({url})"
    except Exception:
        return text

# def get_time():
#     return dt.today().strftime("%A, %d.%m.%Y")

def get_horoscope(target="aries"):
    if target == "none":
        return [0, 0]
    try:
        data = requests.get(f"https://www.thevoicemag.ru/horoscope/daily/{target}")
        soup = BS(data.text, 'html.parser')
        ans = soup.find("div", class_="sign__description-text")
        return [target, ans.text]
    except Exception as err:
        print(err)
        return [0, 0]

# TODO
def get_news():
    ...

def get_horoscopies():
    data = {}
    for hrs in horoscopes:
        key, val = get_horoscope(hrs)
        if key == 0 or val == 0:
            continue
        data[key] = val
    return data

class Weather:
    def __init__(self, title, emoji):
        self.title = title
        self.emoji = emoji

weathers = [
    Weather("ясн", "☀️"),
    Weather("облачн", "⛅️"),
    Weather("дожд", "🌧"),
    Weather("гроз", "⛈"),
    Weather("снег", "🌨")
]

def get_emoji_by_weather(weather: str):
    w = weather.lower()
    emoji = "☁️"
    for ws in weathers:
        if ws.title in w:
            emoji = ws.emoji
    return emoji

def pretty_info(city="msk"):
    finance = ''
    # weather_day = ''
    # weather_now = '\n'
    weather = ''
    valutes = ["EUR", "USD", "AMD", "GEL"] # TODO
    curs_dict = get_finance_rub(valutes)
    bitcoin = get_finance_bitcoin()
    w_data = get_weather_meteoservice_ru(city)
    # TRY MORE
    if not w_data:
        w_data = get_weather_meteoservice_ru(city)
    # h_data = utils.get_ipaddr()
    if not valutes or not bitcoin:
        finance += "Невозможно получить данные о валютах ⚠️"
    else:
        finance += f"""\n_{curs_dict.get('USD')} 💵 \
{curs_dict.get('EUR')} 💶 \
{curs_dict.get('AMD') + ' 🇦🇲 ' if city == 'evn' else ""}\
{curs_dict.get('GEL') + ' 🇬🇪 ' if city == 'tbs' else ""}\
${bitcoin:,} 💎_"""

    holidays = get_holiday()[0]
    if not holidays:
        holidays = "Праздники на сегодня не загрузились ⚠️"
    emoji = ""
    if not w_data:
        weather += "Невозможно загрузить погоду ⚠️"
    else:
        emoji = get_emoji_by_weather(w_data)
        weather = w_data
    buff = f"""*Добрый день!* ☀️
```\tСегодня {holidays}```
\t{finance}

\t{emoji} {weather}

_Ежедневный гороскоп_""" + "\n\t{}\n\n/settings - Настрой бота под себя"
    return buff

def restore(backup, target):
    backup_db = Database(backup)
    target_db = Database(target)
    users = backup_db.get_users_uuids()
    for u in users:
        target_db.login(u[0])
        logger.info(f"User: {u[0]} - restore")

def set_notify_all_users(engine: str):
    db = Database(engine)
    users = db.get_users()
    for u in users:
        db.user_update_notify(u[0], 1)
        logger.debug(f"User: {u[0]} set notify on morning")

# notify value: 1, 2, 4
def get_time_by_notify(notify: int):
    if not notify: return []
    morning = ntv_d.get(1).get("val")
    daytime = ntv_d.get(2).get("val")
    evening = ntv_d.get(4).get("val")
    targets = {
        0: [],
        1: [morning],
        2: [daytime],
        3: [morning, daytime],
        4: [evening],
        5: [morning, evening],
        6: [daytime, evening],
        7: [morning, daytime, evening]
    }
    return targets.get(notify)

def get_timestr_by_notify(notify: int):
    if not notify: return []
    morning = "morning"
    daytime = "daytime"
    evening = "evening"
    targets = {
        0: [],
        1: [morning],
        2: [daytime],
        3: [morning, daytime],
        4: [evening],
        5: [morning, evening],
        6: [daytime, evening],
        7: [morning, daytime, evening]
    }
    return targets.get(notify)

# TODO
def notify_is_enable(user_time: int, time_str: str):
    if time_str in get_timestr_by_notify(user_time):
        return True
    return False

def notify_from_number(user_notify: int):
    targets = {
        1: False,
        2: False,
        4: False,
    }
    match user_notify:
        case 1:
            targets[1] = True
        case 2: 
            targets[2] = True
        case 3:
            targets[1] = True
            targets[2] = True
        case 4:
            targets[4] = True
        case 5:
            targets[1] = True
            targets[4] = True
        case 6:
            targets[2] = True
            targets[4] = True
        case 7:
            targets[1] = True
            targets[2] = True
            targets[4] = True
    return targets

def new_notify_number(targets: dict):
    summa = 0
    for t, enable in targets.items():
        if enable: summa += t
    return summa

def notify_enable(user_notify: int, target: int, switch: str):
    targets = notify_from_number(user_notify)
    if switch == "enable":
        if not targets.get(target):
            targets[target] = True
    else:
        if targets.get(target):
            targets[target] = False
    return new_notify_number(targets)


def get_current_time(city="msk"):
    #return like a "07:00".time()
    delta = timedelta(hours=cities.get(city).get("plus"))
    return dt.strptime(dt.now().strftime("%H:%M") ,"%H:%M") + delta