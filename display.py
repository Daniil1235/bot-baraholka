import main

bot = main.bot
types = main.types


def data(data_list, page_number, items_per_page=5):
    start_index = (page_number - 1) * items_per_page
    end_index = page_number * items_per_page
    page_data = data_list[start_index:end_index]
    keyboard = types.InlineKeyboardMarkup()
    for item in page_data:
        button = types.InlineKeyboardButton(text=f'{item}', callback_data=f"get {str(item)}")
        keyboard.add(button)

    isbtn1 = True
    isbtn2 = True

    if page_number != 1:
        btn_1 = types.InlineKeyboardButton('<--',
                                           callback_data='left')
    else:
        isbtn1 = False
    pass
    if not page_number * items_per_page <= len(data_list) or len(data_list) <= items_per_page:
        isbtn2 = False
    else:
        btn_2 = types.InlineKeyboardButton('-->',
                                           callback_data='right')
    if isbtn1 and isbtn2:
        keyboard.row(btn_1, btn_2)
    elif isbtn1 and not isbtn2:
        keyboard.row(btn_1)
    elif isbtn2 and not isbtn1:
        keyboard.row(btn_2)

    return keyboard


def display_data(message: types.Message, data_list, page_number, items_per_page=5):
    keyboard = data(data_list, page_number, items_per_page)
    bot.send_message(message.chat.id, 'Выберете объявление:', reply_markup=keyboard)


def edit_data(message: types.Message, data_list, page_number, items_per_page=5):
    keyboard = data(data_list, page_number, items_per_page)
    bot.edit_message_reply_markup(message.chat.id, message.id, reply_markup=keyboard)
