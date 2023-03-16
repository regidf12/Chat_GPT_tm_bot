import logging
import sqlite3
import openai
import re
import config

from messages import MESSAGE
from aiogram.types.message import ContentType
from aiogram import Bot, types, Dispatcher
from db import BotDB
from keyboard import kb_sub, kb_follow
from aiogram.utils import executor
from filters import IsAdminFilter

openai.api_key = config.API
model_engine = "text-davinci-003"
logging.basicConfig(level=logging.INFO)
bot = Bot(config.TOKEN)
dp = Dispatcher(bot)
dp.filters_factory.bind(IsAdminFilter)
PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=199 * 100)
DB = BotDB()


async def check(message: types.Message):
    member = await message.bot.get_chat_member(config.CHAT_ID, message.from_user.id)
    return member.is_chat_admin()


async def check_symbols(message: types.Message):
    if await DB.symbol_exists_counter(message.from_user.id) <= 0:
        await bot.send_message(message.chat.id, "Символы: 0")
    else:
        await DB.symbol_exists(message.from_user.id, message)


async def check_follow(message: types.Message):
    if await DB.follower_exists(message.from_user.id) is True:
        return "✅"
    elif await check(message):
        return "👑"
    else:
        return "❌"


async def chat_gpt(message: types.Message):
    prompt = str(message.text)
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2048,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    await bot.send_message(message.chat.id, completion.choices[0].text)


async def dall_e(message: types.Message):
    result = await bot.get_chat_member(chat_id=config.CHAT_ID, user_id=message.from_user.id)
    result_symbol = re.search(r'!', message.text)
    if result['status'] == "left":
        await bot.send_message(message.chat.id,
                               str(message.from_user.first_name) + "Вы не являетесь участником группы",
                               reply_markup=kb_sub)
    else:
        if result_symbol:
            await bot.send_message(message.chat.id, "Ожидайте изображение...")
            prompt = str(message.text)
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512",
            )
            await bot.send_message(message.chat.id, response["data"][0]["url"])
        else:
            await bot.send_message(message.chat.id, "Ожидайте...")
            await chat_gpt(message)


@dp.callback_query_handler(text='get_follower')
async def answer(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, "Напишите мне в лс @Dive_into_dev")


@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url=config.URL,
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await DB.buy_follow(message.from_user.id)
    await bot.send_message(message.chat.id, MESSAGE['follower'])


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await DB.create_table()
    result = await bot.get_chat_member(chat_id=config.CHAT_ID, user_id=message.from_user.id)
    if not DB.user_exists(message.from_user.id):
        DB.add_user(message.from_user.id, message.from_user.first_name)
        if result['status'] == "left":
            await bot.send_message(message.chat.id, "Привет, " + str(message.from_user.first_name) + MESSAGE[
                'start'] + 'Что бы начать подпишись на группу и потом напишите: "/help"',
                                   reply_markup=kb_sub)
        else:
            await bot.send_message(message.chat.id,
                                   "Привет, " + str(message.from_user.first_name) + MESSAGE[
                                       'start'] + 'Что бы начать напишите: "/help"',
                                   reply_markup=kb_sub)
    else:
        if result['status'] == "left":
            await bot.send_message(message.chat.id, "Привет, " + str(message.from_user.first_name) + MESSAGE[
                'start'] + 'Что бы начать подпишись на группу и потом напишите: "/help"',
                                   reply_markup=kb_sub)
        else:
            await bot.send_message(message.chat.id,
                                   "Привет, " + str(message.from_user.first_name) + MESSAGE[
                                       'start'] + 'Что бы начать напишите: "/help"',
                                   reply_markup=kb_sub)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await bot.send_message(message.chat.id, MESSAGE['help'])


@dp.message_handler(is_admin=True, commands=['table'])
async def send_table_with_followers(message: types.Message):
    await DB.get_table(message)


@dp.message_handler(commands=['profile'])
async def send_profile(message: types.Message):
    if await DB.follower_exists(message.from_user.id) is True:
        await bot.send_message(message.chat.id,
                               '🗂 Ваш ID: ' + str(
                                   message.from_user.id) + '\n' + '*️⃣ Ваши символы: ♾' + '\n' +
                               '🔄 Символы обновятся: ' + await DB.get_date_update(
                                   message.from_user.id) + '\n' + '🎫 Состояние подписки: ' + await check_follow(
                                   message) + '\n' + '🕘 Подписка закончится: ' + await DB.get_date_end_follow(
                                   message.from_user.id) + '\n' + '🗓 Вы стали нашим пользователем: ' +
                               await DB.get_date_start(message.from_user.id))
    else:
        await bot.send_message(message.chat.id,
                               '🗂 Ваш ID: ' + str(
                                   message.from_user.id) + '\n' + '*️⃣ Ваши символы: ' + str(
                                   await DB.symbol_exists(message.from_user.id, message)) + '\n' +
                               '🔄 Символы обновятся: ' + await DB.get_date_update(
                                   message.from_user.id) + '\n' + '🎫 Состояние подписки: ' + await check_follow(
                                   message) + '\n' + '🕘 Подписка закончится: ' + await DB.get_date_end_follow(
                                   message.from_user.id) + '\n' + '🗓 Вы стали нашим пользователем: ' +
                               await DB.get_date_start(message.from_user.id), reply_markup=kb_follow)


@dp.message_handler()
async def general(message: types.Message):
    if await DB.symbol_date() is True:
        await DB.symbol()
        await DB.create_symbol_date()
    else:
        pass
    try:
        symbol_counter = len(message.text)
        result = await bot.get_chat_member(config.CHAT_ID, message.from_user.id)
        if result['status'] == "left":
            await bot.send_message(message.chat.id,
                                   str(message.from_user.first_name) + " Вы не являетесь участником группы.",
                                   reply_markup=kb_sub)
        else:
            pass
        if await DB.follow_end_date_exists(message.from_user.id) is True:
            await DB.drop_follow(message.from_user.id)
        else:
            pass
        if await DB.follower_exists(message.from_user.id) is True or check(message):
            await dall_e(message)
        else:
            await DB.symbol_update(message.from_user.id, symbol_counter)
            if await DB.symbol_exists_counter(message.from_user.id) > 0:
                await bot.send_message(message.chat.id, "Ожидайте...")
                await chat_gpt(message)
            else:
                await bot.send_message(message.chat.id,
                                       str(message.from_user.first_name) + " Жаль, но у вас кончились символы.")
    except sqlite3.Error:
        await bot.send_message(message.chat.id,
                               str(message.from_user.first_name) + " Вау, вы нашли баг. Напишите мне: @Dive_into_dev")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
