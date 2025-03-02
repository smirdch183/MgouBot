from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

storage = MemoryStorage()

bot = Bot('6030910548:AAFk9tR_9vSxDqfley-qoSRvaPSA_MG6zF0')
dp = Dispatcher(bot, storage=storage)

class ProfileStatesGroup(StatesGroup):
    photo = State()
    name = State()
    age = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer('Welcom\nнапиши /create')

@dp.message_handler(commands=['create'])
async def cmd_start(message: types.Message) -> None:
    await message.reply('Отправь фото')
    await ProfileStatesGroup.photo.set()

@dp.message_handler(content_types=['photo'], state=ProfileStatesGroup.photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.reply('Отправь имя')
    await ProfileStatesGroup.next()

@dp.message_handler(state=ProfileStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply('Сколько тебе лет')
    await ProfileStatesGroup.next()

@dp.message_handler(state=ProfileStatesGroup.age)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = message.text
    await message.reply('Готово')
    await bot.send_photo(chat_id=message.from_user.id, photo=data['photo'], caption=f"{data['name']}, {data['age']}")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp)