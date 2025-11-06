from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)



async def get_greeting_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text="Добавить питомца 🐶", callback_data="add_pet")],
        [InlineKeyboardButton(text="Посмотреть питомца(-ев) 🐱", callback_data="pets_list")],
    ])
