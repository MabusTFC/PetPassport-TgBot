import aiohttp

from src.config import BASE_URL
from typing import (
    Optional,
    Dict,
    Any,
    List
)

async def register_owner(telegram_id: int, telegram_nick: Optional[str]) -> Optional[int]:
    async with aiohttp.ClientSession() as session:
        payload = {
            "telegramId": telegram_id,
            "telegramNick": telegram_nick
        }
        async with session.post(f"{BASE_URL}/register", json=payload) as resp:
            if resp.status == 200:
                owner_id = await resp.json()
                return owner_id
            print("Ошибка регистрации:", resp.status)
            return None


async def get_owner_by_telegram(telegram_id: int) -> Optional[Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/by-telegram/{telegram_id}") as resp:
            if resp.status == 200:
                return await resp.json()
            print("Владелец не найден:", resp.status)
            return None


async def get_owner_pets(owner_id: int) -> Optional[List[Dict[str, Any]]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/{owner_id}/pets") as resp:
            if resp.status == 200:
                return await resp.json()
            print("Ошибка при получении питомцев:", resp.status)
            return None

async def add_pet(owner_id: int, name: str, breed_: str) -> Optional[Dict[str, Any]]:
    payload = {
        "ownerId": owner_id,
        "name": name,
        "breed": breed_
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/pets/add", json=payload) as resp:
            if resp.status == 200:
                return await resp.json()
            print("Ошибка при добавлении питомца:", resp.status)
            return None