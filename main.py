from bot import bot, notify
import schedule
import asyncio

schedule.every().day.at("07:00").do(notify)

async def scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

async def main():
    print("Service is starting...")
    async_scheduler = asyncio.create_task(scheduler())
    await async_scheduler
    await bot.polling(none_stop=True, timeout=60)

if __name__ == "__main__":
    asyncio.run(main())