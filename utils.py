from main import bot, types


def checksub(message, channel_list, user_id):
    exists = True
    markup = types.InlineKeyboardMarkup()
    for i in channel_list:
        chat_member = bot.get_chat_member(i[0], user_id)
        if chat_member.status == 'left':
            exists = False
            markup.add(types.InlineKeyboardButton(i[1], url=i[2]))
    if not exists:
        markup.add(types.InlineKeyboardButton("✅Я подписался", callback_data="check"))
        bot.send_message(message.chat.id, "Подпишитесь для продолжения", reply_markup=markup)
    else:
        return True


def editsub(message, channel_list, user_id):
    exists = True
    markup = types.InlineKeyboardMarkup()
    for i in channel_list:
        chat_member = bot.get_chat_member(i[0], user_id)
        if chat_member.status == 'left':
            exists = False
            markup.add(types.InlineKeyboardButton(i[1], url=i[2]))
    if not exists:
        markup.add(types.InlineKeyboardButton("✅Я подписался", callback_data="check"))
        bot.edit_message_reply_markup(message.chat.id, message.id, reply_markup=markup)
    else:
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, "✅Готово. Введите комманду повторно")