from main import bot, types
import sqlite3
import main
import datetime


def m(message: types.Message):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users")
    users = cursor.fetchall()
    for i in users:
        if i[1] == str(message.from_user.id):
            if i[3] == 1:
                pass
                if str(datetime.date.today()) == i[4]:
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("Разбан", callback_data="unban"))
                    bot.send_message(message.chat.id, "Нажмите кнопку ниже:", reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, f"Дата разбана: {i[4]}. Попробуйте в эту дату или обратитесьв техподдержку. /support")


