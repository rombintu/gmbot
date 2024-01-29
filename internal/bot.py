import os
from datetime import timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command
# from aiogram.filters import Filter
from internal.content import acivate_message, deactivate_message
from internal import kbs
from internal import Database, logger

from internal.utils import pretty_info, get_horoscopies, notify_enable, get_current_time, get_time_by_notify
# from internal.utils import cities
from dotenv import load_dotenv
load_dotenv()

bot = Bot(os.getenv("TOKEN"), parse_mode=None, disable_web_page_preview=True)
dp = Dispatcher()
# dp.include_routers(user.router, different_types.router)
db = Database(os.getenv("STORE", "sqlite:///db.sqlite"))
ADMIN_ID = 469973030

# Запуск бота
async def start_bot():
    logger.info("Bot is starting...")
    await dp.start_polling(bot)

# # Остановка бота
# async def stop_bot():
#     logger.info("Bot is stopping...")
#     await dp.stop_polling()

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
    await message.answer(
        acivate_message,
    )
    mess = pretty_info(city=user.city)
    await message.answer(
        get_format_message(user, mess), 
        parse_mode="markdown",
    )

@dp.message(Command('deactivate'))
async def handle_message_deactivate(message: types.Message):
    db.deactivate(message.chat.id)
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
        skip = True
        notify_list = get_time_by_notify(u.notify)
        if not notify_list:
            continue
        for tbn in notify_list:
            if tbn <= get_current_time(u.city) <= (tbn + timedelta(seconds=2)):
                skip = False
        if not skip:
            if u.city not in ["msk", None]:
                mess = pretty_info(city=u.city)
            try:
                await bot.send_message(u.uuid, get_format_message(u, mess), parse_mode="markdown")
            except Exception as err:
                logger.warning(err)
                db.delete_user(u)
        # else:
        #     logger.debug(f"Skip user for notify: {u.uuid}")

class Form(StatesGroup):
    content = State()

@dp.message((F.text == '/send') & (F.from_user.id == ADMIN_ID))
async def handler_send_all(message: types.Message, state: FSMContext):
    await state.set_state(Form.content)
    await message.answer("Введи, что отправить всем")

@dp.message(Form.content)
async def send_content(message: types.Message, state: FSMContext):
    content = await state.update_data(content=message.text)
    await state.clear()
    errors = []
    users = db.get_users()
    for u in users:
        try:
            await bot.send_message(u.uuid, content.get("content"), parse_mode="markdown")
        except Exception as err:
            logger.warning(err)
            errors.append(f"{u.uuid}: {err}\n")
    await message.answer(f"Готово. \nWARNS: {[err for err in errors]}")

@dp.callback_query(F.data.startswith("settings_"))
async def callbacks(c: types.CallbackQuery):
    data = c.data.split("_")[1:]
    user = db.get_user(c.message.chat.id)
    async def back():
        await bot.edit_message_text(
                "⚙️ Настройки",
                c.message.chat.id, c.message.message_id,
                reply_markup=kbs.settings()
            )
    match data:
        case ["back"]:
            await back()
        case ["horoscope"]:
            await bot.edit_message_text(
                    "Выбери свой гороскоп",
                    c.message.chat.id, c.message.message_id,
                    reply_markup=kbs.settings_horoscope(user.horoscope)
                )
        case ["horoscope", _]:
            target = data[-1]
            db.user_update_horoscope(c.from_user.id, target)
            await c.answer("Настройки сохранены")
            await back()
        case ["city"]:
            await bot.edit_message_text(
                    "Выбери свой город",
                    c.message.chat.id, c.message.message_id,
                    reply_markup=kbs.settings_city(user.city)
                )
        case ["city", _]:
            target = data[-1]
            db.user_update_city(c.from_user.id, target)
            await c.answer("Настройки сохранены")
            await back()
        case ["notify"]:
            # user = db.get_user(c.message.chat.id)
            if not user:
                await c.answer("Пользователя уже не существует")
            await bot.edit_message_text(
                    "Когда должны приходить уведомления",
                    c.message.chat.id, c.message.message_id,
                    reply_markup=kbs.settings_notify(user.notify)
                )
        case ["notify", _, _]:
            switch = data[-1]
            notify_value = int(data[-2])
            # user = db.get_user(c.message.chat.id)
            if not user:
                await c.answer("Пользователя уже не существует")
            new_notify_value = notify_enable(user.notify, notify_value, switch)
            db.user_update_notify(user.uuid, new_notify_value)
            user = db.get_user(c.message.chat.id)
            await c.answer("Настройки сохранены")
            await bot.edit_message_reply_markup(
                    c.message.chat.id, c.message.message_id,
                    reply_markup=kbs.settings_notify(user.notify)
                )
    await c.answer()