import requests
import datetime
import locale
import socket

from bs4 import BeautifulSoup as BS
import netifaces as ni

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


# def get_ipaddr():
#     try:
#         hostname = socket.gethostname()
#         ipaddr = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']
#         return [hostname, ipaddr]
#     except Exception as err:
#         print(err)
#         return []

def get_time():
    return datetime.datetime.today().strftime("%A, %d.%m.%Y")