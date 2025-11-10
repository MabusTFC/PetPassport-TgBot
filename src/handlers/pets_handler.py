from gc import callbacks

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Router, F, types

from src.keyboard.keyboard import get_pets_list_keyboard, get_my_pet_keyboard
from src.utils.api_client import get_owner_pets, get_owner_by_telegram

router = Router()

@router.callback_query(lambda c: c.data == "pets_list")
async def pets_list(callback_query: CallbackQuery, state = FSMContext):
    tg_id = callback_query.from_user.id
    owner_data = await get_owner_by_telegram(tg_id)
    owner_id = owner_data['ownerId']
    pets = await get_owner_pets(owner_id)


    if not pets:
        await callback_query.answer("У вас пока нет питомцев!")
        return
    elif len(pets) == 1:
        await callback_query.answer(f"You have {len(pets)} pets")
    elif len(pets) > 1:

        await callback_query.message.answer_photo(
            photo=FSInputFile("img/zaglushka.jpg"),
            caption="📋 Выбери питомца:",
            parse_mode="Markdown",
            reply_markup=await get_pets_list_keyboard(pets),
        )

@router.callback_query(F.data.startswith("pet_"))
async def handle_pet_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()  
    pet_id = int(callback_query.data.split("_")[1])

    await callback_query.message.answer_photo(
        photo=FSInputFile("img/zaglushka.jpg"),
        caption=f"🐾 Вы выбрали питомца с ID: {pet_id}",
        parse_mode="Markdown",
        reply_markup=await get_my_pet_keyboard(pet_id),
    )
