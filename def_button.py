from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

start_sticker = 'CAACAgIAAxkBAAIrQGQvqjIAAUnT6L-AXIEkVVd1zC-5oAACQCIAAnq2YEur-eo2cza__i8E'
watering_sticker = 'CAACAgIAAxkBAAIrQmQvu0VKwCBwNvwGTKuEbncRg-1kAAJsKQACIi6oSisOSJbTYGATLwQ'

HELP_COMMAND = """

🌳 <b>Добавить дерево:</b> Добавьте новое дерево в список всех деревьев 
💦 <b>Обработать:</b> Используйте эту команду чтобы обработать выбранное вами дерево
🍁 <b>Показать список деревьев:</b> Показать список всех деревьев в саду
🧾 <b>Список команд:</b> Выберите чтобы увидеть все команды в нашем саду
🔍 <b>Место сада: </b> Показывает локацию нашего сада
✏  <b>Удалить дерево: </b> Удаляет дерево по выбранным координатам

"""

menu = '''
🔥  <b>Приветствую тебя в нашем саду</b>, выбирай действия с садом🌳

🌳 <b>Добавить дерево:</b> Добавьте новое дерево в список всех деревьев 
💦 <b>Обработать:</b> Используйте эту команду чтобы обработать выбранное вами дерево
🍁 <b>Показать список деревьев:</b> Показать список всех деревьев в саду
🧾 <b>Список команд:</b> Выберите чтобы увидеть все команды в нашем саду
🔍 <b>Место сада: </b> Показывает локацию со всеми деревьями в саду
✏  <b>Удалить дерево: </b> Удаляет дерево по выбранным координатам
  


'''
#==================================================================================================
# кнопка для random znak
kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb2.add(KeyboardButton('/help'))
# кнопка для help
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('/help')).insert(KeyboardButton('/start')).insert(KeyboardButton('/trees')).insert(
    KeyboardButton('/add')).insert(KeyboardButton('/location')).insert(KeyboardButton('/treatment'))

# =========================================
# inline кнопочки для /start
ikb = InlineKeyboardMarkup(row_width=2)

ib1 = InlineKeyboardButton(text='Добавить дерево🌲',
                           callback_data='add'
                           )

ib2 = InlineKeyboardButton(text='Обработать💦',
                           callback_data='treatment'
                           )
ib3 = InlineKeyboardButton(text='Показать список деревьев🍁',
                           callback_data='trees'
                           )
ib5 = InlineKeyboardButton(text='Расположение дерева🔍 ',
                           callback_data='location'
                           )
ib6 = InlineKeyboardButton(text='Удалить дерево✏ ',
                           callback_data='delete'
                           )
ikb.add(ib1, ib2, ib3, ib5, ib6)
