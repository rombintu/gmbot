import requests
import datetime
import locale
from store.store import Database

from bs4 import BeautifulSoup as BS
from content import horoscopes

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

def get_finance_rub():
    try:
        req = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        return (req['Valute']['USD']['Value'], req['Valute']['EUR']['Value'])
    except Exception as err:
        print(err)
        return (0, 0)

def get_finance_bitcoin():
    try:
        req = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCRUB').json()
        return int(req['price'].split(".")[0])
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

# def get_weather_to_day():
#     try:
#         data = requests.get("https://meteoinfo.ru/forecasts/russia/moscow-area/moscow")
#         soup = BS(data.text, 'html.parser')
#         ans = soup.find_all("tr")[6]
#         weather = ans.find_all("i")
#         w_value = weather[0].text
#         w_string = weather[1].text
#         w_winter = weather[-1].text
#         return [w_value, w_string, w_winter]
#     except Exception as err:
#         print(err)
#         return []
    
# def get_weather_to_now():
#     try:
#         data = requests.get("https://www.yandex.ru/pogoda/moscow?lat=55.755863&lon=37.6177")
#         soup = BS(data.text, 'html.parser')
#         # ans = soup.find("div", class_="fact card card_size_big")
#         weather = soup.find("div", class_="temp fact__temp fact__temp_size_s").text
#         return [weather]
#     except Exception as err:
#         print(err)
#         return []
def weather_org(weather: str):
    w = weather.split(";")
    try:    
        w.remove("…")
        w.pop(0)
    except: pass

    try:
        return [w[1], w[3], w[5], w[-1]]
    except Exception as err:
        print(err)
        return []

def get_weather_yandex():
    try:
        data = requests.get("https://www.yandex.ru/pogoda/details/10-day-weather?lat=55.755863&lon=37.6177&via=mf")
        soup = BS(data.text, 'html.parser')
        ans = soup.find("table", class_="weather-table")
        tbody = ans.find_all("tr", class_="weather-table__row")
        meta = ["morning", "day", "evening", "night"]
        parsing_data = {}
        for row, met in zip(tbody, meta):
            parsing_data[met] = weather_org(row.getText(separator=";"))
        return parsing_data
    except Exception as err:
        print(err)
        return {}

def get_weather_meteoservice_ru():
    url = "https://www.meteoservice.ru/weather/today/moskva"
    data = requests.get(url)
    soup = BS(data.text, "html.parser")
    text = soup.find("strong").text
    return text + f"\n[Метеосервис.ру Москва]({url})"

def get_time():
    return datetime.datetime.today().strftime("%A, %d.%m.%Y")

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
    emoji = "🌸"
    for ws in weathers:
        if ws.title in w:
            emoji = ws.emoji
    return emoji

def pretty_info():
    finance = ''
    # weather_day = ''
    # weather_now = '\n'
    weather = ''
    usd, eur = get_finance_rub()
    bitcoin = get_finance_bitcoin()
    w_data = get_weather_meteoservice_ru()
    # TRY MORE
    if not w_data:
        w_data = get_weather_meteoservice_ru()
    # h_data = utils.get_ipaddr()
    if not usd or not eur or not bitcoin:
        finance += "Невозможно получить данные о валютах ⚠️"
    else:
        finance += f"\n_{round(usd, 2)}$ | {round(eur, 2)}€ | {bitcoin:,}₿_"

    holidays = get_holiday()[0]
    if not holidays:
        holidays = "Праздники на сегодня не загрузились ⚠️"
    # if not w_data:
    #     weather_day += "Невозможно загрузить дневную погоду ⚠️"
    # else:
    #     weather_day += f"Днем *{w_data[0]}°C*\n_{w_data[-1]}_\n{w_data[1]}"
    
    if not w_data:
        weather += "Невозможно загрузить погоду ⚠️"
    else:
        emoji = get_emoji_by_weather(w_data)
        weather = w_data
    buff = f"""*Доброе утро!* ☀️
```\tСегодня {holidays}```
\t{finance}

\t{emoji} {weather}

_Ежедневный гороскоп_. Чтобы настроить /settings""" + "\n\t{}"
    return buff

def restore(backup, target):
    backup_db = Database(backup)
    target_db = Database(target)
    users = backup_db.get_users_uuids()
    for u in users:
        target_db.login(u[0])
        print(f"User: {u[0]} - restore")
