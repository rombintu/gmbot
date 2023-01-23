# Internal
import os, sys
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
    

    usd, eur = utils.get_finance_rub()
    bitcoin = utils.get_finance_bitcoin()
    w_data = utils.get_weather()
    # h_data = utils.get_ipaddr()
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

    

    buff = f"Доброе утро!\n*{utils.get_time()}*"
    buff += f"\nСегодня {holiday}"
    buff += finance + "\n"
    buff += weather
    return buff


load_dotenv()
bot = Bot(os.getenv("TOKEN"))
# clients = sys.argv[1:]
clients = [469973030, 750163152]

def run():
    for i, cl in enumerate(clients):
        bot.send_message(pretty_info(), int(cl))

if __name__ == "__main__":
    schedule.every().day.at("07:00").do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)