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


def get_pets_list_keyboard(pets: list[dict]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=pet["name"], callback_data=f"pet_{pet['id']}")]
        for pet in pets
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_my_pet_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text="Редактировать информацию о питомце 🐶", callback_data="settings_my_pet")],
        [InlineKeyboardButton(text="Посмотреть питомца(-ев) 🐱", callback_data="pets_list")],
    ])

async def get_settings_pet_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text="Имя", callback_data="add_pet")],
        [InlineKeyboardButton(text="Порода", callback_data="pets_list")],
        [InlineKeyboardButton(text="Вес", callback_data="add_pet")],
        [InlineKeyboardButton(text="Возраст", callback_data="add_pet")],
        [InlineKeyboardButton(text="Фото", callback_data="add_pet")]
    ])
