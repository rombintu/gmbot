from bot import bot, notify
import schedule
import threading, time, logging

schedule.every().day.at("07:00").do(notify)

def scheduler():
    logging.info("Scheduler is starting...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    sch = threading.Thread(target=scheduler)
    sch.start()
    logging.info("Service is starting...")
    bot.polling(none_stop=True, timeout=60)
    