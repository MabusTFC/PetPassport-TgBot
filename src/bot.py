import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import (
    auth_handler,
    add_pet_handler,
    pets_handler
)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(auth_handler.router)
    dp.include_router(add_pet_handler.router)
    dp.include_router(pets_handler.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
