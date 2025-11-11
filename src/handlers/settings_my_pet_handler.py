from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from src.keyboard.keyboard import get_settings_pet_keyboard
from src.states.update_pet_info_states import EditPetStates
from src.utils.api_client import update_pet

router = Router()


pending_edits: dict[int, dict] = {} #глобальная хуйня

@router.callback_query(lambda c: c.data.startswith("settings_my_pet_"))
async def settings_pet_handler(callback_query: CallbackQuery, state: FSMContext):
    pet_id = int(callback_query.data.split("_")[-1])
    await state.update_data(pet_id=pet_id)

    await callback_query.message.answer_photo(
        photo=FSInputFile("img/zaglushka.jpg"),
        caption="📋 Выбери, что хочешь изменить:",
        parse_mode="Markdown",
        reply_markup=await get_settings_pet_keyboard(pet_id)
    )
    await state.set_state(EditPetStates.choosing_field)
    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith("edit_field_"))
async def start_edit_field(callback_query: CallbackQuery):
    _, _, field, pet_id = callback_query.data.split("_")
    pet_id = int(pet_id)

    prompts = {
        "name": "✏️ Введи новое имя питомца:",
        "breed": "🐾 Введи новую породу питомца:",
        "weight": "⚖️ Введи новый вес питомца:",
        "birth": "🎂 Введи новую дату рождения (YYYY-MM-DD):"
    }

    await callback_query.message.answer(
        prompts.get(field, "Введи новое значение:")
    )

    pending_edits[callback_query.from_user.id] = {"pet_id": pet_id, "field": field}
    await callback_query.answer()


@router.message()
async def process_field_update(message: Message):
    user_id = message.from_user.id

    edit_data = pending_edits[user_id]
    pet_id = edit_data["pet_id"]
    field = edit_data["field"]
    value = message.text.strip()

    kwargs = {}
    if field == "name":
        kwargs["name"] = value
    elif field == "breed":
        kwargs["breed"] = value
    elif field == "weight":
        try:
            kwargs["weight_kg"] = float(value.replace(",", "."))
        except ValueError:
            await message.answer("⚠️ Вес должен быть числом (например 4.5).")
            return
    elif field == "birth":
        from datetime import datetime
        try:
            datetime.strptime(value, "%Y-%m-%d")
            kwargs["birth_date"] = value
        except ValueError:
            await message.answer("⚠️ Формат даты должен быть YYYY-MM-DD.")
            return

    success = await update_pet(pet_id, **kwargs)
    if success:
        await message.answer("✅ Информация успешно обновлена!")
    else:
        await message.answer("❌ Ошибка при обновлении.")

    del pending_edits[user_id]
