import sqlite3
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from def_button import *
import config as cfg

con = sqlite3.connect('database.db')
cursor = con.cursor()


cursor.execute(
    '''CREATE TABLE IF NOT EXISTS trees (id INTEGER PRIMARY KEY, 
    tree_type TEXT, 
    age INTEGER, 
    health INTEGER, 
    size_x INTEGER, 
    size_y INTEGER,
    watering BOOLEAN DEFAULT FALSE)
    ''')
# Токен бота
token = cfg.token


class Form(StatesGroup):
    text = State()
    koor = State()
    latlon = State()
    delete = State()
    # Задаем состояние


bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(_):
    print('Бот запущен')

@dp.message_handler(commands=['add'])
async def add_tree(message: types.Message):
    await bot.send_message(message.chat.id,
                           '<b>Введите данные дерева через пробел (Вид, Возраст, Здоровье, Широта, Долгота)</b>\nПример: Береза 23 100 140 30',
                           parse_mode='html')
    await Form.text.set()  # Устанавливаем состояние

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    global sticker_id
    sticker_id = (await bot.send_sticker(message.chat.id, start_sticker)).message_id
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    await bot.send_message(chat_id=message.from_user.id, parse_mode='html', text=menu, reply_markup=ikb)


@dp.message_handler(commands=['trees'])
async def trees(message: types.Message):
    cursor.execute('''SELECT * FROM trees ORDER BY tree_type ASC''')
    rows = cursor.fetchall()
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(e)
    await bot.send_message(message.chat.id, '<b>Вид, возраст, здоровье, широта, долгота</b>', parse_mode='html')
    text = ''
    for i, row in enumerate(rows):
        text += f'{i + 1}. {row[1].title()} {row[2]} {row[3]} {row[4]} {row[5]}\n'
    await bot.send_message(message.chat.id, text)


@dp.message_handler(commands=['location'])
async def locations(message: types.Message):
    global water_sticker_id, sticker_id
    try:
        await bot.delete_message(message.chat.id, water_sticker_id)
    except Exception as e:
        print(e)
    try:
        await bot.delete_message(message.chat.id, sticker_id)
    except Exception as e:
        print(e)
    await bot.send_message(message.chat.id, '<b>Введите координаты дерева</b>', parse_mode='html')
    cursor.execute('''SELECT * FROM trees ORDER BY tree_type ASC''')
    rows = cursor.fetchall()
    text = ''
    for i, row in enumerate(rows):
        text += f'{i + 1}. {row[1].title()} {row[4]} {row[5]}\n'
    await bot.send_message(message.chat.id, text)
    await Form.latlon.set()  # Устанавливаем состояние
@dp.message_handler(state=Form.latlon)
async def get_latlon(message: types.Message, state = FSMContext):
    async with state.proxy() as proxy:  # Устанавливаем состояние ожидания
        proxy['latlon'] = message.text
    await state.finish()
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    try:
        await bot.delete_message(message.chat.id, message.message_id)
        lat = message.text.split()[0]
        lon = message.text.split()[1]
        await bot.send_location(chat_id=message.from_user.id, latitude=lat, longitude=lon)

    except Exception as e:
        print(e)


@dp.message_handler(state=Form.text)  # Принимаем состояние
async def get_tree(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:  # Устанавливаем состояние ожидания
        proxy['text'] = message.text
    await state.finish()
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    try:
        type = message.text.split()[0]  # Получаем вид дерева
        age = message.text.split()[1]  # Получаем возраст дерева
        health = message.text.split()[2]  # Получаем здоровье дерева
        size_x = message.text.split()[3]  # Получаем ширину дерева
        size_y = message.text.split()[4]  # Получаем высоту дерева
    except IndexError:
        await message.answer('Данные были введены некорректно. Попробуйте еще раз.')
    try:
        cursor.execute(
            '''INSERT INTO trees (tree_type, age, health, size_x, size_y, watering) VALUES (?, ?, ?, ?, ?, ?)''',
            (type, age, health, size_x, size_y, False))
        con.commit()
        await bot.send_message(message.chat.id, 'Дерево успешно добавлено👍')
    except Exception as e:
        print(e)
@dp.message_handler(commands=['delete'])
async def get_deleting_tree(message: types.Message):
    try:
        await bot.send_message(message.chat.id, '<b>Введите координаты дерева:</b>', parse_mode='html')
        cursor.execute('''SELECT * FROM trees ORDER BY tree_type ASC''')
        rows = cursor.fetchall()
        text = ''
        for i, row in enumerate(rows):
            text += f'{i + 1}. {row[1].title()} {row[4]} {row[5]}\n'
        await bot.send_message(message.chat.id, text)
        await Form.delete.set()
    except Exception as e:
        print(e)

@dp.message_handler(state = Form.delete)
async def delete_tree(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:  # Устанавливаем состояние ожидания
        proxy['delete'] = message.text
    await state.finish()
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    try:
        lat = message.text.split()[0]
        lon = message.text.split()[1]
        cursor.execute('''DELETE FROM trees WHERE size_x = ? AND size_y = ?''', (lat, lon))
        con.commit()
        await bot.send_message(message.chat.id, 'Дерево успешно удалено👍')
    except Exception as e:
        print(e)



@dp.message_handler(commands=['treatment'])
async def treatment(message: types.Message):
    global sticker_id
    await bot.delete_message(message.chat.id, message.message_id)
    try:
        await bot.delete_message(message.chat.id, sticker_id)
    except Exception as e:
        print(e)
    global water_sticker_id
    water_sticker_id = (await bot.send_sticker(message.chat.id, watering_sticker)).message_id
    await bot.send_message(message.chat.id, '<b>Выберите дерево для обработки(введите <em>КООРДИНАТЫ</em> через пробел)</b>', parse_mode='html')
    cursor.execute('''SELECT * FROM trees ORDER BY tree_type ASC''')
    rows = cursor.fetchall()
    await bot.send_message(message.chat.id, '<b>Вид, широта, долгота:</b>', parse_mode='html')
    with open('trees.txt', 'w') as f:
        for i, row in enumerate(rows):
            f.write(f'{i + 1}. {row[1].title()} {row[4]} {row[5]}\n')
    with open('trees.txt', 'r') as f:
        await bot.send_message(message.chat.id, f.read() + '\n')
    await Form.koor.set()


@dp.message_handler(state=Form.koor)
async def get_koor(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:  # Устанавливаем состояние ожидания
        proxy['koor'] = message.text
    await state.finish()
    try:
        size_x = message.text.split()[0]
        size_y = message.text.split()[1]
        cursor.execute('''SELECT * FROM trees WHERE size_x = ? AND size_y = ?''', (size_x, size_y))
        rows = cursor.fetchone()

        if rows is None:
            await bot.send_message(message.chat.id, 'Дерево не найдено')
        else:
            await bot.send_message(message.chat.id, 'Дерево обработано!✅')
    except Exception as e:
        await message.answer('Данные были введены некорректно. Попробуйте еще раз.')


@dp.callback_query_handler()
async def callback_tostart(callback: types.CallbackQuery):
    if callback.data == 'add':
        await add_tree(message=callback.message)
    elif callback.data == 'treatment':
        await treatment(message=callback.message)
    elif callback.data == 'trees':
        await trees(message=callback.message)
    elif callback.data == 'location':
        await locations(message=callback.message)
    elif callback.data == 'help':
        await send_help(message=callback.message)
    elif callback.data == 'delete':
        await get_deleting_tree(message=callback.message)


# безкомандный
@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_sticker(
        chat_id=message.from_user.id,
        sticker='CAACAgIAAxkBAAIqoGQuXK9uFeVUe2v2T-F6qSIs9VGSAAKdLQACuDVJSTiX7l6tU2mHLwQ'

    )
    await message.reply('Такой команды нет :( '
                        ' <b>Напишите</b> /start для ознакомления с командами',
                        reply_markup=kb2, parse_mode='html'
                        )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
