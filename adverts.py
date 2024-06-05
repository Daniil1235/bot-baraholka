from main import bot, types


def m(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🎲случайные", callback_data="random")
    btn2 = types.InlineKeyboardButton("🔎Поиск определённых", switch_inline_query_current_chat="")
    btn3 = types.InlineKeyboardButton("🆓бесплатные/договорные", callback_data="free")
    markup.row(btn1, btn2)
    markup.row(btn3)
    bot.send_message(message.chat.id, "Какие объявления вы хототе посмотреть?", reply_markup=markup)
