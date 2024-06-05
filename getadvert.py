import sqlite3
import main

bot = main.bot
types = main.types


def m(message: types.Message):
    text = message.text.replace("/getadvert ", "")
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    exists = False
    for i in items:
        if str(i[0]) == text:
            exists = True
            photo = open(f"photos/{i[1]} - {i[2]}.png", "rb")
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("🛒хочу приобрести", callback_data=f"buy {i[0]}")
            btn2 = types.InlineKeyboardButton("🔎Искать ещё", switch_inline_query_current_chat="")
            markup.row(btn1, btn2)
            bot.send_photo(message.chat.id, photo, caption=f"{i[2]} \n"
                                                           f"Цена : {i[4]} \n"
                                                           f"{i[3]}", reply_markup=markup)
    if not exists:
        bot.send_message(message.chat.id, "Не найдено")

