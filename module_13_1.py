from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

api =''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
buy_button = KeyboardButton(text="Купить")
kb.add(button)
kb.add(button2)
kb.add(buy_button)

kb2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать колории', callback_data='colories')],
        [InlineKeyboardButton(text='Формула рассчёта', callback_data='formulas')]])

kb3 = InlineKeyboardMarkup(
    inline_keyboard=[

        [InlineKeyboardButton(text='Product1', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product2', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product3', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product4', callback_data="product_buying")]])





@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию: ', reply_markup=kb2)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        await message.answer(f'Название Product{i} |Описание: описание {i} Цена: {i * 100} ')
        with open(f'files/product{i}.png', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки: ', reply_markup=kb3)


@dp.callback_query_handler(text='colories')
async def set_age(call):
    await call.message.answer('Ввидите свой возраст')
    await UserState.age.set()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 * вес + 6.25 * рост - 5 * возраст + 5')


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=kb)


@dp.callback_query_handler(text='colories')
async def set_age(call):
    await call.message.answer('Ввидите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_colories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    weight = data['weight']
    growth = data['growth']
    colories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваша норма колорий является {colories}')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
