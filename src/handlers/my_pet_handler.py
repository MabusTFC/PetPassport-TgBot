from aiogram import (
    F,
    Router,
    types
)

from aiogram.types import (
    FSInputFile,
    callback_query
)

from src.keyboard.keyboard import get_my_pet_keyboard

router = Router()


@router.callback_query(F.data.startswith("pet_"))
async def handle_pet_callback(callback: types.CallbackQuery):
    pet_id = int(callback.data.split("_")[1])

    await callback_query.answer_photo(
        photo=FSInputFile("img/zaglushka.jpg"),
        caption=f"🐾 Вы выбрали питомца с ID: {pet_id}",
        parse_mode="Markdown",
        reply_markup=await get_my_pet_keyboard(),
    )