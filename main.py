import asyncio
import logging
import sys
from os import getenv
from datetime import datetime
import time
import schedule

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.main_kb import main_kb, admin_kb
from states.main_states import Main
from database.db import get_all_tg_ids, set_time_sub, add_user, get_sub_status
from yokass.linknid import check, create

TOKEN = "7239822620:AAHROpIE3EGdB3iOIfywnDEq6RLGBkZAW0M"

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

list_admins = [6157416760, 6639790624, 5436978766, 6864449629]

CHANNEL_ID = -1002195056770

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    print(get_all_tg_ids())
    add_user(message.from_user.id)

    if message.from_user.id not in list_admins:
        await message.answer(text='Сообщение на /start', reply_markup=main_kb)
    else:
        await message.answer(text='Сообщение на /start', reply_markup=admin_kb)


async def check_channel_members():
    member_ids = get_all_tg_ids()

    for member in member_ids:
        if member in list_admins:
            continue

        tg_id = member
        if not get_sub_status(tg_id):
            payment_url, payment_id = create(1, tg_id)

            payment_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Оплатить', url=payment_url)],
            [InlineKeyboardButton(text='Проверить оплату', callback_data=f'check_{payment_id}')]
            ])
            await bot.ban_chat_member(CHANNEL_ID, tg_id)
            await bot.send_message(chat_id = tg_id, text='У вас истекла подписка! Вы были исключены из закрытого канала, для возвращения оплатите следующий месяц.', reply_markup=payment_kb)


def schedule_checks():
    schedule.every().day.at("00:00").do(lambda: asyncio.run(check_channel_members()))

# Запуск планировщика
async def scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


@dp.message(F.text == 'Отзывы')
async def reviews(message: Message) -> None:
    await message.answer(text='https://t.me/D2Svip_feedback\nСсылка на группу для отзывов')


@dp.message(F.text == 'Курс ¥')
async def rates(message: Message) -> None:
    f = open('bd.txt')
    rates = f.read()
    f.close
    await message.answer(text=f'Актуальный курс: <b>{rates}</b>')


@dp.message(F.text == 'Логистики')
async def logist(message: Message) -> None:
    await message.answer(text='''машина 10-12 дней 🚚 ( 790 рублей/кг )
авиа доставка 3-5 дней ✈️ ( 1800/кг )
супер-экспресс 48 часов 🚀 ( 2000/кг )
''')


@dp.message(F.text == 'Информация о канале')
async def info_about_channel(message: Message) -> None:
    await message.answer(text='''### Преимущества подписки D2Svip 📦

Откройте новые возможности для бизнеса с нашей подпиской! Получите доступ к эксклюзивному обучению и логистическим решениям, которые помогут вам эффективно заказывать товары с Poizon и других маркетплейсов.

Что вы получите: ✅

- Эксклюзивное обучение: В нашем телеграм-канале вас ждут обучающие видеоролики по заказу товаров и обмену валют, которые помогут вам быстро освоить все необходимые процессы и сэкономить ваше время.

- Преимущества для реселлеров: 👟 Наша подписка идеально подходит для реселлеров. Получите доступ к лучшим логистическим партнёрам и выбирайте из множества вариантов доставки:
  - Машина: 10-12 дней 🚚
  - Экспресс авиа: 3-5 дней ✈️
  - Супер экспресс: 48 часов 🚀
  Количество доступных логистических решений постоянно увеличивается!

- Выгодный обмен валют: 💸 Участникам нашего закрытого телеграм-канала доступен обмен валют с лучшим курсом юаня на рынке (на 06.09.2024 курс 12.4). Такого курса вы не найдёте нигде!

- Уникальные возможности выкупа: Вы сможете выкупать товары с значком (≈) из других стран, пользуясь нашими особыми условиями логистики. 🇺🇸

- Полная поддержка логистики: Мы полностью берем на себя заботу о доставке. Всё, что вам нужно — получить уникальный код клиента и выбрать логистику. Мы доставим товар вам или вашему клиенту через СДЭК. 🌐

- Круглосуточная поддержка: Наша команда D2Svip support всегда готова помочь вам с любыми вопросами, касающимися обучения или логистики. 

Присоединяйтесь к D2Svip прямо сейчас и начните заказывать товары выгодно и быстро!

С нами вы получите:
- Лучшие цены 💲
- Быструю доставку 🚀
- Полную поддержку 🤝

Не упустите шанс стать нашим партнёром и вывести ваш бизнес на новый уровень! 📦
''')


@dp.message(F.text == 'Купить доступ 490р/месяц')
async def buy(message: Message) -> None:
    payment_url, payment_id = create(1, message.from_user.id)

    payment_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Оплатить', url=payment_url)],
    [InlineKeyboardButton(text='Проверить оплату', callback_data=f'check_{payment_id}')]
    ])
    
    await message.answer(text='В стоимость подписки входит обучение по заказу товаров, а так же все логистики ( включая экспресс 48 часов ) и обменник валют', reply_markup=payment_kb)


@dp.callback_query(lambda c: 'check' in c.data)
async def check_handler(callback: CallbackQuery):
    result = check(callback.data.split('_')[-1])
    if not result:
        await callback.message.answer('Оплата еще не прошла или возникла ошибка')
    else:
        await bot.unban_chat_member(chat_id = CHANNEL_ID, user_id = callback.from_user.id, only_if_banned=True)
        time_sub = int(time.time()) + 2592000
        set_time_sub(tg_id=callback.from_user.id, time_sub=time_sub)
        link = await bot.create_chat_invite_link(chat_id = CHANNEL_ID, member_limit=1)
        await callback.message.answer(f'Оплата прошла успешно! Вот ссылка для вступления в закрытый канал:\n{link.invite_link}')

@dp.message(F.text == 'Задать курс ¥')
async def set_rates(message: Message, state: FSMContext) -> None:
    await message.answer(text='Введите курс:')
    await state.set_state(Main.exchange_rate)


@dp.message(Main.exchange_rate)
async def get_rates(message: Message, state: FSMContext) -> None:
    f = open('bd.txt', 'w')
    f.write(message.text)
    f.close()
    await message.answer(text='Курс был успешно изменён')
    await state.set_state(Main.default)


async def main() -> None:
    # Запуск планировщика в параллельной задаче
    asyncio.create_task(scheduler())

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    # Настройка планировщика
    schedule_checks()

    # Запуск бота и планировщика
    asyncio.run(main())