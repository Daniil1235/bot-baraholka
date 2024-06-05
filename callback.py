import sqlite3
import main
import os
import random
import display
import utils
import config

bot = main.bot
types = main.types

id = ""
name = ""


def m(callback: types.CallbackQuery):
    global id
    global name
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    if "change" in callback.data:
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        for i in items:
            if callback.data == f"change {i[0]}":
                id = i[0]
                name = i[2]
                bot.send_message(callback.message.chat.id, "Введите новое имя")
                bot.register_next_step_handler(callback.message, change)

    elif "price" in callback.data:
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        for i in items:
            if callback.data == f"price {i[0]}":
                id = i[0]
                bot.send_message(callback.message.chat.id, "Введите новую цену")
                bot.register_next_step_handler(callback.message, price)

    elif "delete" in callback.data:
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        for i in items:
            if callback.data == f"delete {i[0]}":
                id = i[0]
                bot.send_message(callback.message.chat.id, "Вы уверены? для удаление введите yes , для отмены - no")
                bot.register_next_step_handler(callback.message, delete)

    elif "deluser" in callback.data:
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        for i in users:
            if callback.data == f"deluser {i[0]}":
                id = i[1]
                bot.send_message(callback.message.chat.id, "Вы уверены? для удаление введите yes , для отмены - no")
                bot.register_next_step_handler(callback.message, deluser)

    elif callback.data == "random":
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        if not items:
            bot.send_message(callback.message.chat.id, "Нет объявлений☹️")
            return None
        i = random.choice(items)
        photo = open(f"photos/{i[1]} - {i[2]}.png", "rb")
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("🛒хочу приобрести", callback_data=f"buy {i[0]}")
        btn2 = types.InlineKeyboardButton("🎲ещё", callback_data="random")
        markup.row(btn1, btn2)

        bot.send_photo(callback.message.chat.id, photo, caption=f"{i[2]} \n"
                                                                f"Цена : {i[4]} \n"
                                                                f"{i[3]}", reply_markup=markup)

    elif "buy" in callback.data:
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        for i in items:
            if callback.data == f"buy {i[0]}":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✅да, отправить", callback_data=f"request {i[1]} - {i[2]}"))
                bot.send_message(callback.message.chat.id, "чтобы связаться с продавцом ,нужно отправить ему запрос. для отмены проигнорируйте это сообщение", reply_markup=markup)

    elif callback.data == "right":
        cursor.execute(f'SELECT page_number FROM users WHERE tg = "{callback.message.chat.id}"')
        page_number = cursor.fetchall()[0][0]
        cursor.execute(f'UPDATE users SET page_number = "{page_number + 1}" WHERE tg = "{callback.message.chat.id}"')
        connection.commit()
        cursor.execute(f'SELECT data_list FROM users WHERE tg = "{callback.message.chat.id}"')
        data_list = eval(cursor.fetchall()[0][0])
        display.edit_data(callback.message, data_list=data_list, page_number=page_number + 1)

    elif callback.data == "left":
        cursor.execute(f'SELECT page_number FROM users WHERE tg = "{callback.message.chat.id}"')
        page_number = cursor.fetchall()[0][0]
        cursor.execute(f'UPDATE users SET page_number = "{page_number - 1}" WHERE tg = "{callback.message.chat.id}"')
        connection.commit()
        cursor.execute(f'SELECT data_list FROM users WHERE tg = "{callback.message.chat.id}"')
        data_list = eval(cursor.fetchall()[0][0])
        display.edit_data(callback.message, data_list=data_list, page_number=page_number - 1)


    elif "get" in callback.data:
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        message = callback.message
        for i in items:
            if callback.data == f"get {i[2]}":
                if i[1] == str(message.chat.id):
                    photo = open(f"photos/{message.chat.id} - {i[2]}.png", "rb")
                    markup = types.InlineKeyboardMarkup()
                    btn1 = types.InlineKeyboardButton("✏️изменить имя",
                                                      callback_data=f"change {i[0]}")
                    btn2 = types.InlineKeyboardButton("💲изменить цену",
                                                      callback_data=f"price {i[0]}")
                    btn3 = types.InlineKeyboardButton("❌удалить объявление",
                                                      callback_data=f"delete {i[0]}")
                    markup.row(btn1, btn2, btn3)

                    bot.send_photo(message.chat.id, photo, caption=f"{i[2]} \n"
                                                                   f"Цена : {i[4]} \n"
                                                                   f"{i[3]}", reply_markup=markup)
    elif "update" in callback.data:
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        for i in users:
            if callback.data == f"update {i[0]}":
                id = i[0]
                bot.send_message(callback.message.chat.id, "доступно только по промокоду")

    elif callback.data == "eval":
        bot.send_message(callback.message.chat.id, "введите комманду на выполнение (Осторожно ! Прямй доступ к хостингу!")
        bot.register_next_step_handler(callback.message, evall)

    elif callback.data == "exec":
        bot.send_message(callback.message.chat.id, "введите комманду на выполнение (Осторожно ! Прямй доступ к хостингу!")
        bot.register_next_step_handler(callback.message, execc)

    elif callback.data == "ban":
        bot.send_message(callback.message.chat.id, "введите tg id")
        bot.register_next_step_handler(callback.message, bann)

    elif callback.data == "unban":
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        for i in users:
            if i[1] == str(callback.message.chat.id):
                cursor.execute(f'UPDATE users SET banned = "{0}" WHERE tg = "{i[1]}"')
                cursor.execute(f'UPDATE users SET unban_data = "{0}" WHERE tg = "{i[1]}"')
                bot.send_message(callback.message.chat.id, "успешно")

    elif "request" in callback.data:
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        for i in users:
            if i[1] in callback.data:
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton("✅разрешить", callback_data=f"allow {callback.message.chat.id}")
                btn2 = types.InlineKeyboardButton("❌Запретить", callback_data=f"deny {callback.message.chat.id}")
                markup.row(btn1, btn2)
                bot.send_message(i[1], f"Пользователь \"{callback.message.chat.first_name}\" Хочет связаться с вами для покупки объявления \"{callback.data.split(' ')[3]}\"", reply_markup=markup)
                bot.send_message(callback.message.chat.id, "Запрос отправлен. Ожидайте ответа")
                bot.edit_message_reply_markup(callback.message.chat.id, callback.message.id, reply_markup=None)

    elif "allow" in callback.data:
        bot.send_message(callback.data.split(" ")[1], f"Ваш запрос принят. Телеграм продваца: @{callback.message.chat.username}")
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.id, reply_markup=None)
        bot.send_message(callback.message.chat.id, "✅запрос принят")

    elif "deny" in callback.data:
        bot.send_message(callback.data.split(" ")[1], f"Ваш запрос отклонён")
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.id, reply_markup=None)
        bot.send_message(callback.message.chat.id, "❌запрос отклонён")

    elif callback.data == "free":
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        for i in users:
            if i[1] == str(callback.message.chat.id):
                if i[2] != 0:
                    markup = types.InlineKeyboardMarkup()
                    btn1 = types.InlineKeyboardButton("бесплатные", switch_inline_query_current_chat="FREE")
                    btn2 = types.InlineKeyboardButton("договорные", switch_inline_query_current_chat="PRICE")
                    markup.row(btn1, btn2)
                    bot.send_message(callback.message.chat.id, "нажмите на кнопку", reply_markup=markup)
                else:
                    bot.send_message(callback.message.chat.id, "повысьте привилегию")

    elif callback.data == "check":
        utils.editsub(callback.message, config.channels, callback.message.chat.id)

    connection.commit()
    cursor.close()
    connection.close()


def change(message: types.Message):
    global id
    global name
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Операция отменена")
        return None

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'UPDATE items SET name = "{message.text}" WHERE id = "{id}"')
    bot.send_message(message.chat.id, "Успешно обновлено")
    connection.commit()
    os.rename(f"photos/{message.chat.id} - {name}.png", f"photos/{message.chat.id} - {message.text}.png")
    cursor.close()
    connection.close()


def price(message: types.Message):
    global id
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Операция отменена")
        return None
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'UPDATE items SET price = "{message.text}" WHERE id = "{id}"')
    connection.commit()
    cursor.close()
    connection.close()
    bot.send_message(message.chat.id, "Успешно обновлено")


def delete(message: types.Message):
    global id
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Операция отменена")
        return None
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    if message.text == "yes":
        cursor.execute(f'DELETE FROM items WHERE id = "{id}"')
        bot.send_message(message.chat.id, "Успешно удалено")
    else:
        bot.send_message(message.chat.id, "Удаление отменено")

    connection.commit()
    cursor.close()
    connection.close()


def deluser(message: types.Message):
    global id
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Операция отменена")
        return None
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    if message.text == "yes":
        connection.commit()
        cursor.execute(f'DELETE FROM items WHERE user_id = "{id}"')
        cursor.execute(f'DELETE FROM users WHERE tg = "{id}"')
        connection.commit()
        bot.send_message(message.chat.id, "Успешно удалено")


    else:
        bot.send_message(message.chat.id, "Удаление отменено")

    connection.commit()
    main.start(message)
    cursor.close()
    connection.close()


def evall(message: types.Message):
    try:
        bot.send_message(message.chat.id, str(eval(message.text)))
    except Exception as e:
        bot.send_message(message.chat.id, f"необрабатываемое исключение: \n {e}")


def execc(message: types.Message):
    try:
        exec(message.text)
    except Exception as e:
        bot.send_message(message.chat.id, f"необрабатываемое исключение: \n {e}")


def bann(message):
    global id
    id = message.text
    bot.send_message(message.chat.id, "введите дату разбана в формате ГГГГ-ММ-ДД")
    bot.register_next_step_handler(message, date)


def date(message: types.Message):
    global id
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    date = message.text
    try:
        d = date.split("-")
        i = int(d[0])
        if 2023 < i < 2050:
            i = int(d[1])
            if 0 < i < 12:
                i = int(d[2])
                if 0 < i < 31:
                    cursor.execute(f'UPDATE users SET banned = "1" WHERE tg = "{id}"')
                    cursor.execute(f'UPDATE users SET unban_data = "{date}" WHERE tg = "{id}"')
                    bot.send_message(id, "Вы были забанены!")
                    bot.send_message(message.chat.id, "успешно")
                else:
                    bot.send_message(message.chat.id, f"неверная дата")
            else:
                bot.send_message(message.chat.id, f"неверная дата")
        else:
            bot.send_message(message.chat.id, f"неверная дата")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: \n {e}")


    connection.commit()
    cursor.close()
    connection.close()
