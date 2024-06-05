from main import bot, types
import sqlite3
import main


name = ""
desc = ""
price = ""
photo = ""


def m(message: types.Message):
    bot.send_message(message.chat.id, "Введите название")
    bot.register_next_step_handler(message, namee)


def namee(message: types.Message):
    global name
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Операция отменена")
        return None

    name = message.text
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    exists = False
    for i in items:
        if name == i[2] and str(message.from_user.id) == i[1]:
            exists = True
            break

    if exists:
        bot.send_message(message.chat.id, "такой товар сущетвует! повторите попытку")
        return None
    else:
        bot.send_message(message.chat.id, "теперь введите описание.")
        bot.register_next_step_handler(message, descc)


def descc(message):
    global desc
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Операция отменена")
        return None
    desc = message.text
    bot.send_message(message.chat.id, "теперь введите цену. Вы можете написать 'бесплатно ' или 'договорная'")
    bot.register_next_step_handler(message, pricee)


def pricee(message: types.Message):
    global price
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Операция отменена")
        return None
    price = message.text
    if not price.isdigit():
        if price != "бесплатно" and price != "договорная":
            bot.send_message(message.chat.id, "Попробуйте ещё раз!")
            bot.register_next_step_handler(message, pricee)
            return None
    bot.send_message(message.chat.id, "теперь отправьте фото товара")
    bot.register_next_step_handler(message, photoo)


def photoo(message: types.Message):
    global photo
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Операция отменена")
        return None

    def save_photo(filename):
        try:
            ph = message.photo[-1]
            file_info = bot.get_file(ph.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            save_path = f'photos/{filename}.png'
            with open(save_path, 'wb') as new_file:
                new_file.write(downloaded_file)
        except Exception:
            bot.send_message(message.chat.id, "повторите попытку!")
            bot.register_next_step_handler(message, photoo)
            return "error"

    path = f"{message.from_user.id} - {name}"
    if save_photo(path) == "error":
        return None

    photo = path

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO items(user_id, name, description, photo, price) VALUES ("{message.from_user.id}", "{name}", "{desc}", "{photo}", "{price}")')
    bot.send_message(message.chat.id, "Объявление опубликовано")
    connection.commit()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    for i in items:
        if i[3] == desc:
            id = i[0]
            break
    i = types.InlineQueryResultArticle(
        id=f'{id}', title=f"{name}",
        description=f"{desc}",
        input_message_content=types.InputTextMessageContent(
            message_text=f"/getadvert {id}"))
    main.results.append(i)



    cursor.close()
    connection.close()
