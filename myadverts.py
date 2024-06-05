import display
from main import bot, types
import sqlite3
import main


def m(message: types.Message):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    exists = False

    data_list = []
    for i in items:

        if i[1] == str(message.from_user.id):
            exists = True
            data_list.append(i[2])

    if not exists:
        bot.send_message(message.chat.id, "У вас нет объявлений!")
    else:
        cursor.execute(f'UPDATE users SET page_number = "{1}" WHERE tg = "{message.from_user.id}"')
        cursor.execute(f'UPDATE users SET data_list = "{data_list}" WHERE tg = "{message.from_user.id}"')
        connection.commit()
        cursor.execute(f'SELECT page_number FROM users WHERE tg = "{message.from_user.id}"')
        page_number = cursor.fetchall()[0][0]

        display.display_data(message, data_list= data_list, page_number= page_number)
