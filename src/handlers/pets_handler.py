from gc import callbacks

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Router

from src.keyboard.keyboard import get_pets_list_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "pets_list")
async def pets_list(callback_query: CallbackQuery, state = FSMContext):
    data = await state.get_data()
    owner = data.get("owner_id")

    pets = owner.get("pets",[])

    if not pets:
        await callback_query.answer("У вас пока нет питомцев!")
        return
    elif len(pets) == 1:
        await callback_query.answer(f"You have {len(pets)} pets")
    elif len(pets) > 1:

        await callback_query.answer_photo(
            photo=FSInputFile("img/zaglushka.jpg"),
            caption="📋 Выбери питомца:",
            parse_mode="Markdown",
            reply_markup=await get_pets_list_keyboard(pets),
        )
