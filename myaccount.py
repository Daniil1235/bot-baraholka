import sqlite3
import main

bot = main.bot
types = main.types

name = ""
phone = ""
email = ""
password = ""


def m(message: types.Message):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    for i in users:
        if i[1] == str(message.from_user.id):
            if i[2] == 0:
                privilegy = "Обычный"
            elif i[2] == 1:
                privilegy = "Премиум"
            elif i[2] == 2:
                privilegy = "админ"


    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🆕обновление привилегии", callback_data=f"update {i[0]}")
    btn2 = types.InlineKeyboardButton("❌удалить пользователя", callback_data=f"deluser {i[0]}")

    markup.row(btn1, btn2)


    bot.send_message(message.chat.id, f"Ваши данные: \n"
                                      f"Имя: {message.from_user.first_name}\n"
                                      f"Привилегия: {privilegy}\n"
                                      f"Выберете действие:", reply_markup=markup)
