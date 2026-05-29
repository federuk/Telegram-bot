import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Отправь текст, затем 2 ссылки (каждое сообщение отдельно)")

@dp.message(Command("reset"))
async def reset_counter(message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {
        "step": 0,
        "data": [],
        "counter": 1
    }
    await message.answer("Счётчик сброшен")

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {
            "step": 0,
            "data": [],
            "counter": 1
        }

    state = user_data[user_id]

    state["data"].append(message.text)
    state["step"] += 1

    if state["step"] == 3:
        text = state["data"][0]
        link1 = state["data"][1]
        link2 = state["data"][2]

        result = f"{state['counter']}) {text}\n\n{link1}\n{link2}"

        await message.answer(result)

        state["counter"] += 1
        state["step"] = 0
        state["data"] = []

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
