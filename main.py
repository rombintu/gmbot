import functools
import aioschedule
import asyncio
import signal
import sys

from internal import logger
from content import notify_timers_values
from bot import start_bot, notify, db

def exit(signame, loop):
    logger.warning(f'Received {signame} signal. Cancelling all tasks...')
    for task in asyncio.all_tasks():
        logger.info(f"Task: {task.get_name()} is stopped...")
        task.cancel()
    try:
        loop.stop()
        sys.exit(0)
    except RuntimeError as err:
        logger.error(err)

async def run_bot():
    await start_bot()

# TODO scheduler
async def scheduler():
    for ntv in notify_timers_values.values():
        aioschedule.every().day.at(ntv).do(notify)
    # aioschedule.every().minute.do(notify) # DEV
    logger.info("Scheduler is starting...")
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def handle_signals():
    loop = asyncio.get_running_loop()
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(exit, signame, loop))


async def main():
    scheduler_task = scheduler()
    bot_task = asyncio.create_task(run_bot(), name="Bot")
    handle_signals_task = asyncio.create_task(handle_signals(), name="Handler signals")

    tasks = [scheduler_task, bot_task, handle_signals_task]
    group_tasks = asyncio.gather(*tasks)
    try:
        await group_tasks
    except KeyboardInterrupt:
        logger.info("Received SIGINT signal. Cancelling all tasks...")
        group_tasks.cancel()
    except Exception as err:
        logger.error(err)
        group_tasks.cancel()

# TODO
if __name__ == "__main__":
    logger.info("Service is starting...")
    asyncio.run(main())


