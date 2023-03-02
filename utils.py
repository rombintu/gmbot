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

def get_weather():
    try:
        data = requests.get("https://meteoinfo.ru/forecasts/russia/moscow-area/moscow")
        soup = BS(data.text, 'html.parser')
        ans = soup.find_all("tr")[6]
        weather = ans.find_all("i")
        w_value = weather[0].text
        w_string = weather[1].text
        w_winter = weather[-1].text
        return [w_value, w_string, w_winter]
    except Exception as err:
        print(err)
        return []

def get_time():
    return datetime.datetime.today().strftime("%A, %d.%m.%Y")

def get_horoscope(target="aries"):
    try:
        data = requests.get(f"https://www.thevoicemag.ru/horoscope/daily/{target}")
        soup = BS(data.text, 'html.parser')
        ans = soup.find("div", class_="sign__description-text")
        return [target, ans.text]
    except Exception as err:
        print(err)
        return []

def get_horoscopies():
    data = {}
    for hrs in horoscopes:
        key, val = get_horoscope(hrs)
        data[key] = val
    return data

def pretty_info():
    finance = '\n'
    weather = '\n'

    usd, eur = get_finance_rub()
    bitcoin = get_finance_bitcoin()
    w_data = get_weather()
    # h_data = utils.get_ipaddr()
    if not usd or not eur or not bitcoin:
        finance += "Невозможно получить данные о валютах ⚠️"
    else:
        finance += f"\n_{round(usd, 2)}$ | {round(eur, 2)}€ | {bitcoin:,}₿_"

    holidays = get_holiday()
    if not holidays:
        holidays = ["Праздники не загружаются ⚠️", "Праздники не загружаются ⚠️"]
    if not w_data:
        weather += "Невозможно загрузить погоду ⚠️"
    else:
        weather += f"*{w_data[0]}°C*\n_{w_data[-1]}_\n{w_data[1]}"

    

    buff = f"*Доброе утро!*\n"
    buff += f'\n```\tСегодня {holidays[0]}\n\tЗавтра {holidays[-1]}```'
    buff += finance + "\n"
    buff += weather
    buff += "\n\n_Ежедневный гороскоп_. Чтобы настроить /settings\n\t```{}```"
    return buff

def restore(backup, target):
    backup_db = Database(backup)
    target_db = Database(target)
    users = backup_db.get_users_uuids()
    for u in users:
        target_db.login(u[0])
        print(f"User: {u[0]} - restore")
