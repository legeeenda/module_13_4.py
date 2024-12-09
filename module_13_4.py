from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio


API_TOKEN = '7787493433:AAGBdEiUhUvCcydfXXxFbbS_F_T_Ca5Tfbk'


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class UserState(StatesGroup):
    age = State()   
    growth = State() 
    weight = State() 


@dp.message(Command("start"))
async def set_age(message: types.Message, state: FSMContext):
    await message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)  


@dp.message(UserState.age)
async def set_growth(message: types.Message, state: FSMContext):

    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост (в сантиметрах):")
    await state.set_state(UserState.growth)  


@dp.message(UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):

    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес (в килограммах):")
    await state.set_state(UserState.weight)  


@dp.message(UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):

    await state.update_data(weight=int(message.text))
    

    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']

    bmr = 10 * weight + 6.25 * growth - 5 * age - 161


    await message.answer(f"Ваша норма калорий: {bmr:.2f} ккал.")
    

    await state.clear()


async def main():
    print("Bot is running...")
    await bot.delete_webhook(drop_pending_updates=True)  
    await dp.start_polling(bot)  
if __name__ == "__main__":
    asyncio.run(main())
