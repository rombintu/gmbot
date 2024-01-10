from bot import start_bot, stop_bot, notify
import aioschedule
import asyncio
from internal import logger
import signal

time_for_scheduler = "07:00"

# async def bot_run():
#     logger.info("Bot is starting...")
#     try:
#         await dp.start_polling(bot)
#     except KeyboardInterrupt:
#         logger.info("Bot is stopping...")


# TODO scheduler
async def scheduler():
    aioschedule.every().day.at(time_for_scheduler).do(notify)
    # aioschedule.every().minute.do(notify) # DEV
    logger.info("Scheduler is starting...")
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

def handle_sigint():
    logger.info("Received SIGINT signal. Cancelling all tasks...")
    for task in asyncio.all_tasks():
        task.cancel()

async def main():
    c1 = scheduler()
    c2 = start_bot()
    try:
        await asyncio.gather(c1, c2)
        # await asyncio.gather(c1)
    except KeyboardInterrupt:
        logger.info("Received SIGINT signal. Cancelling all tasks...")
        for task in asyncio.all_tasks():
            task.cancel()
        await asyncio.gather(*asyncio.all_tasks())

# TODO
if __name__ == "__main__":
    logger.info("Service is starting...")
    signal.signal(signal.SIGINT, lambda s, f: asyncio.create_task(handle_sigint(), stop_bot()))
    asyncio.run(main())
    
