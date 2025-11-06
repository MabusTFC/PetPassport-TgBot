from aiogram import Router

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from states.add_pet_states import AddPetStates
from utils.api_client import  add_pet

router = Router()


@router.callback_query(lambda c: c.data == "add_pet")
async def balance_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    owner_id = data.get("owner_id")
    tg_id = data.get("tg_id")


    await state.update_data(owner_id=owner_id["ownerId"])
    await callback_query.answer("Введите импя питомца: ")
    await state.set_state(AddPetStates.waiting_for_name)


@router.callback_query(AddPetStates.waiting_for_name)
async def process_name(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(name = callback_query.text)
    await callback_query.answer("✨ Укажи вид питомца (например: кошка, собака):")
    await state.set_state(AddPetStates.waiting_for_type)


@router.callback_query(AddPetStates.waiting_for_type)
async def process_type(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    owner_id = data["owner_id"]
    name = data["name"]
    type_ = callback_query.text

    result = await add_pet(owner_id, name, type_)
    await state.clear()