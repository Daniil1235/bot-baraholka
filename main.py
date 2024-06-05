from telebot import TeleBot, types
import config
import sqlite3

bot = TeleBot(config.BOT_TOKEN)

results = []
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM items")
items = cursor.fetchall()
for i in items:
    results.append(types.InlineQueryResultArticle(
        id=f'{i[0]}', title=f"{i[2]}",
        description=f"{i[3]}",
        input_message_content=types.InputTextMessageContent(
            message_text=f"/getadvert {i[0]}")))

import abcd
import addadvert
import adverts
import myadverts
import callback
import myaccount
import getadvert
import admin
import unban
import utils


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    if utils.checksub(message, config.channels, message.from_user.id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        connection.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users 
                          (id INTEGER PRIMARY KEY, 
                          tg TEXT, privelegy INTEGER(1), 
                          banned INTEGER(1), 
                          unban_data VARCHAR(8), 
                          page_number INTEGER, 
                          data_list TEXT)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS items 
                          (id INTEGER PRIMARY KEY, 
                          user_id TEXT, 
                          name VARCHAR(30), 
                          description TEXT, 
                          price VARCHAR(10), 
                          photo TEXT)""")

        connection.commit()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        exists = False
        for i in users:
            pass
            if i[1] == str(message.from_user.id):
                exists = True

        if not exists:
            cursor.execute(f'INSERT INTO users(tg, privelegy, banned, unban_data, page_number, data_list) VALUES ("{message.from_user.id}", "0", "0", "0", "1", "[]")')
        connection.commit()
        cursor.close()
        connection.close()
        code = message.text.replace("/start ", "")
        if code == "123488":
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute(f'UPDATE users SET privelegy = "{1}" WHERE tg = "{message.from_user.id}"')
            connection.commit()
            cursor.close()
            connection.close()
            bot.send_message(message.chat.id, "Премиум активирован")
        else:
            bot.send_message(message.chat.id, "привет. Используй меню комманд")


@bot.message_handler(commands=["adverts"])
def advertt(message: types.Message):
    if utils.checksub(message, config.channels, message.from_user.id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for i in users:
            if i[1] == str(message.from_user.id):
                if i[3] == 1:
                    bot.send_message(message.chat.id, "Вы забанены. /unban")
                    return None
        adverts.m(message)


@bot.message_handler(commands=["myadverts"])
def myadvertss(message: types.Message):
    if utils.checksub(message, config.channels, message.from_user.id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for i in users:
            if i[1] == str(message.from_user.id):
                if i[3] == 1:
                    bot.send_message(message.chat.id, "Вы забанены. /unban")
                    return None
        myadverts.m(message)


@bot.message_handler(commands=["addadvert"])
def addadvertt(message: types.Message):
    if utils.checksub(message, config.channels, message.from_user.id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for i in users:
            if i[1] == str(message.from_user.id):
                if i[3] == 1:
                    bot.send_message(message.chat.id, "Вы забанены. /unban")
                    return None
        addadvert.m(message)


@bot.message_handler(commands=["myaccount"])
def myaccountt(message: types.Message):
    if utils.checksub(message, config.channels, message.from_user.id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for i in users:
            if i[1] == str(message.from_user.id):
                if i[3] == 1:
                    bot.send_message(message.chat.id, "Вы забанены. /unban")
                    return None
        myaccount.m(message)


@bot.message_handler(commands=["cancel"])
def cancel(message: types.Message):
    bot.send_message(message.chat.id, "Никаких операций не запланировано")


@bot.callback_query_handler(func=lambda call: True)
def callbackk(call):
    callback.m(call)


@bot.message_handler(commands=["getadvert"])
def geradvertt(message):
    if utils.checksub(message, config.channels, message.from_user.id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for i in users:
            if i[1] == str(message.from_user.id):
                if i[3] == 1:
                    bot.send_message(message.chat.id, "Вы забанены. /unban")
                    return None
        getadvert.m(message)


@bot.message_handler(commands=["admin"])
def adminn(message):
    admin.m(message)


@bot.message_handler(commands=["unban"])
def unbann(message: types.Message):
    unban.m(message)


@bot.message_handler(content_types=["text"])
def text(message: types.Message):
    bot.send_message(message.chat.id, "Сейчас не запланировано никаких операций. Введите какую-нибудь комманду")


@bot.inline_handler(func=lambda query: True)
def query_text(query: types.InlineQuery):
    text = query.query
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    global results
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    if text == "FREE":
        r = []
        for i in items:
            if i[4] == "бесплатно":
                for q in results:
                    if int(q.id) == i[0]:
                        r.append(q)
        bot.answer_inline_query(query.id, r)
    elif text == "PRICE":
        r = []
        for i in items:
            if i[4] == "договорная":
                for q in results:
                    if int(q.id) == i[0]:
                        r.append(q)
        bot.answer_inline_query(query.id, r)
    else:
        r = []
        for i in items:
            if text in i[2] or text in i[3]:
                for q in results:
                    if int(q.id) == i[0]:
                        r.append(q)
        bot.answer_inline_query(query.id, r)


bot.polling(none_stop=True)
