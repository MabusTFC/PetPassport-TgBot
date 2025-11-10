import ssl

import aiohttp


from src.config import BASE_URL
from typing import (
    Optional,
    Dict,
    Any,
    List
)

async def register_owner(telegram_id: int, telegram_nick: Optional[str]) -> Optional[int]:
    payload = {
        "telegramId": telegram_id,
        "telegramNick": telegram_nick or "Unknown"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/api/Owners/register", json=payload) as resp:
            print("Ответ сервера при регистрации владельца:", resp.status)
            if resp.status in (200, 201):
                data = await resp.json()
                print("Ответ JSON:", data)

                # если сервер вернул просто число — сразу возвращаем
                if isinstance(data, int):
                    return data
                # если вернул объект — достаем id
                return data.get("id")
            else:
                print("Ошибка регистрации:", resp.status, await resp.text())
                return None


async def get_owner_by_telegram(telegram_id: int) -> Optional[Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/api/Owners/by-telegram/{telegram_id}") as resp:
            if resp.status == 200:
                return await resp.json()
            print("Владелец не найден:", resp.status)
            return None


async def get_owner_pets(owner_id: int) -> Optional[List[Dict[str, Any]]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/api/Owners/{owner_id}/pets") as resp:
            if resp.status == 200:
                return await resp.json()
            print("Ошибка при получении питомцев:", resp.status)
            return None

async def add_pet(owner_id: int, name: str, breed: str):
    payload = {
        "name": name,
        "breed": breed,
        "ownerId": int(owner_id)
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/api/Pets", json=payload) as resp:
            print(f"Ответ сервера: {resp.status}")
            if resp.status in (200, 201):  # иногда backend возвращает 201 Created
                return await resp.json()
            else:
                text = await resp.text()
                print("Ошибка при добавлении питомца:", text)
                return None

async def update_pet(pet_id: int,
                     name: str = None,
                     breed: str = None,
                     weight_kg: float = None,
                     birth_date: str = None
                     ) -> bool:
    payload = {}

    if name:
        payload["name"] = name
    if breed:
        payload["breed"] = breed
    if weight_kg:
        payload["weightKg"] = weight_kg
    if birth_date:
        payload["birthDate"] = birth_date

    if not payload:
        return False

    async with aiohttp.ClientSession() as session:
        async with session.put(f"{BASE_URL}/api/Pets/{pet_id}", json=payload) as resp:
            if resp.status == 200:
                return True
            print("Ошибка при обновлении питомца:", resp.status)
            return False