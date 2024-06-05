from main import bot, types
import sqlite3
import main


def m(message: types.Message):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM USERS")
    users = cursor.fetchall()
    for i in users:
        if i[1] == str(message.from_user.id):
            pass
            if i[2] != 2:
                bot.send_message(message.chat.id, "недоступно для вашего аккаунта")
                return None

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("eval", callback_data="eval")
    btn2 = types.InlineKeyboardButton("exec", callback_data="exec")
    btn3 = types.InlineKeyboardButton("ban", callback_data="ban")
    markup.row(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Выберете опцию", reply_markup=markup)
