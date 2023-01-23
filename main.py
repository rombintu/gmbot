# Internal
import os
import time
# Local
from bot import Bot
import utils

# External
from dotenv import load_dotenv
import schedule

def pretty_info():
    finance = '\n'
    holiday = '\n'
    weather = '\n'
    host_data = '\n'

    usd, eur = utils.get_finance_rub()
    bitcoin = utils.get_finance_bitcoin()
    w_data = utils.get_weather()
    h_data = utils.get_ipaddr()
    if not usd or not eur or not bitcoin:
        finance += "Невозможно получить данные о валютах ⚠️"
    else:
        finance += f"\n_{round(usd, 2)}$ | {round(eur, 2)}€ | {bitcoin:,}₿_"

    holidays = utils.get_holiday()
    if not holidays:
        holiday += "Праздники не загружаются ⚠️"
    else:
        holiday = holidays[0]

    if not w_data:
        weather += "Невозможно загрузить погоду ⚠️"
    else:
        weather += f"Погода: *{w_data[0]}* _{w_data[-1]}_\n{w_data[1]}"

    if not h_data:
        host_data += "\nИнтерфейс не подключен ⚠️"
    else:
        host_data += f"\n`{h_data[0]}` : `{h_data[1]}`"

    buff = f"Доброе утро!\n*{utils.get_time()}*"
    buff += f"\nСегодня {holiday}"
    buff += finance + "\n"
    buff += weather
    buff += host_data
    return buff


load_dotenv()
bot = Bot(os.getenv("TOKEN"), os.getenv("UUID"))

def run():
    bot.send_message(pretty_info())

if __name__ == "__main__":
    schedule.every().day.at("14:53").do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)