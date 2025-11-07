from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data == "settings_my_pet")
async def settings_pet_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    owner_id = data.get("owner_id")


@router.callback_query(lambda c: c.data == "settings_pet_name")
async def settings_pet_name(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

@router.callback_query(lambda c: c.data == "settings_pet_breed")
async def settings_pet_breed(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

@router.callback_query(lambda c: c.data == "settings_pet_weight")
async def settings_pet_weight(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

@router.callback_query(lambda c: c.data == "settings_pet_age")
async def settings_pet_age(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

@router.callback_query(lambda c: c.data == "settings_pet_photo")
async def settings_pet_photo(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
