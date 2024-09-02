from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отзывы')],
    [KeyboardButton(text='Курс ¥'),
    KeyboardButton(text='Логистики')],
    [KeyboardButton(text='Информация о канале')],
    [KeyboardButton(text='Купить доступ 490р/месяц')]
], resize_keyboard=True)

admin_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отзывы')],
    [KeyboardButton(text='Курс ¥'),
    KeyboardButton(text='Логистики')],
    [KeyboardButton(text='Информация о канале')],
    [KeyboardButton(text='Купить доступ 490р/месяц')],
    [KeyboardButton(text='Задать курс ¥')]
], resize_keyboard=True)