from bot import bot, notify
import schedule

def main():
    schedule.every().day.at("07:00").do(notify)
    schedule.run_pending()
    print("Service is starting...")
    bot.polling(none_stop=True, timeout=60)

if __name__ == "__main__":
    main()