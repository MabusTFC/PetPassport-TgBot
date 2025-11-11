
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Router, F, types

from src.keyboard.keyboard import get_pets_list_keyboard, get_my_pet_keyboard
from src.utils.search_data import get_pet_data

router = Router()

@router.callback_query(lambda c: c.data == "pets_list")
async def pets_list(callback_query: CallbackQuery, state = FSMContext):
    tg_id = callback_query.from_user.id
    pets = await get_pet_data(tg_id)

    if not pets:
        await callback_query.answer("У вас пока нет питомцев!")
        return

    elif len(pets) == 1:
        pet = pets[0]
        pet_id = pet["id"]
        await callback_query.message.answer_photo(
            photo=FSInputFile("img/zaglushka.jpg"),
            caption=f"🐾 Питомец: {pet['name']}\nПорода: {pet.get('breed', 'не указана')}",
            parse_mode="Markdown",
            reply_markup=await get_my_pet_keyboard(pet_id),
        )
        await callback_query.answer()
        return

    elif len(pets) > 1:
        await callback_query.message.answer_photo(
            photo=FSInputFile("img/zaglushka.jpg"),
            caption="📋 Выбери питомца:",
            parse_mode="Markdown",
            reply_markup=await get_pets_list_keyboard(pets),
        )
        await callback_query.answer()

@router.callback_query(F.data.startswith("pet_"))
async def handle_pet_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    tg_id = callback_query.from_user.id
    pet_id = int(callback_query.data.split("_")[1])

    pet = await get_pet_data(tg_id, pet_id)

    await callback_query.message.answer_photo(
        photo=FSInputFile("img/zaglushka.jpg"),
        caption=f"🐾 Питомец: {pet['name']}\nПорода: {pet.get('breed', 'не указана')}",
        parse_mode="Markdown",
        reply_markup=await get_my_pet_keyboard(pet_id),
    )





