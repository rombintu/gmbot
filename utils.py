import requests
import datetime
import locale

from bs4 import BeautifulSoup as BS

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

def get_holiday():
    try:
        data = requests.get("https://www.calend.ru/")
        soup = BS(data.text, 'html.parser')
        ans = soup.find("ul", class_="itemsNet").find("span", "title").\
            getText().split(":")[-1].split(",")
        return ans
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


def pretty_info():
    finance = '\n'
    holiday = '\n'
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
        holiday += "Праздники не загружаются ⚠️"
    else:
        holiday = holidays[0].strip()

    if not w_data:
        weather += "Невозможно загрузить погоду ⚠️"
    else:
        weather += f"Погода: *{w_data[0]}* _{w_data[-1]}_\n{w_data[1]}"

    

    buff = f"Доброе утро!\n*{get_time()}*"
    buff += f"\nСегодня {holiday}"
    buff += finance + "\n"
    buff += weather
    return buff