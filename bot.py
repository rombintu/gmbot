import os

from aiogram import Bot, Dispatcher, types, F
# from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from content import acivate_message, deactivate_message
from internal import kbs
from internal import db, logger

from utils import pretty_info, get_horoscopies
from dotenv import load_dotenv
load_dotenv()

bot = Bot(os.getenv("TOKEN"), parse_mode=None, disable_web_page_preview=True)
dp = Dispatcher()
# dp.include_routers(user.router, different_types.router)

# Запуск бота
async def start_bot():
    logger.info("Bot is starting...")
    await dp.start_polling(bot)

# Остановка бота
async def stop_bot():
    logger.info("Bot is stopping...")
    await dp.stop_polling()

def get_format_message(user, mess):
    hrs = get_horoscopies()
    hrs_user = "Гороскопы отключены"
    if user["horoscope"] != "none":
        hrs_user = hrs[user.horoscope]
    return mess.format(hrs_user)

@dp.message(Command('start', 'activate'))
async def handle_message_start(message: types.Message):
    db.login(message.chat.id)
    user = db.get_user(message.chat.id)
    mess = pretty_info(city=user.get('city'))
    await message.answer(
        acivate_message,
    )
    await message.answer(
        get_format_message(user, mess), 
        parse_mode="markdown",
    )

@dp.message(Command('deactivate'))
async def handle_message_deactivate(message: types.Message):
    await db.deactivate(message.chat.id)
    await message.answer(
        deactivate_message
    )

@dp.message(Command('try'))
async def handle_message_try(message: types.Message):
    user = db.get_user(message.chat.id)
    mess = pretty_info(city=user.city)
    await message.answer(
        get_format_message(user, mess),
        parse_mode="markdown"
    )

@dp.message(Command("settings"))
async def handle_message_settings(message: types.Message):
    await message.answer(
        "⚙️ Настройки",
        reply_markup=kbs.settings(),
    )

async def notify():
    users = db.get_users()
    mess = pretty_info()
    for u in users:
        try:
            await bot.send_message(u.uuid, get_format_message(u, mess), parse_mode="markdown")
        except Exception as err:
            print(err)
            await db.delete_user(u)

async def send_all(message: types.Message):
    users = db.get_users()
    for u in users:
        try:
            await bot.send_message(u.uuid, message, parse_mode="markdown")
        except Exception as err:
            print(err)

@dp.callback_query(F.data.startswith("settings_"))
async def callbacks(c: types.CallbackQuery):
    data = c.data.split("_")[1:]
    match data:
        case ["horoscope"]:
            await bot.edit_message_text(
                    "Выбери свой гороскоп",
                    c.message.chat.id, c.message.message_id,
                    reply_markup=kbs.settings_horoscope()
                )
        case ["horoscope", _]:
            target = data[-1]
            db.user_update_horoscope(c.from_user.id, target)
            await c.answer("Настройки сохранены")
            await bot.edit_message_text(
                    "⚙️ Настройки",
                    c.message.chat.id, c.message.message_id,
                    reply_markup=kbs.settings()
                )
        case ["city"]:
            await bot.edit_message_text(
                    "Выбери свой город",
                    c.message.chat.id, c.message.message_id,
                    reply_markup=kbs.settings_city()
                )
        case ["city", _]:
            target = data[-1]
            db.user_update_city(c.from_user.id, target)
            await c.answer("Настройки сохранены")
            await bot.edit_message_text(
                    "⚙️ Настройки",
                    c.message.chat.id, c.message.message_id,
                    reply_markup=kbs.settings()
                )
    await c.answer()