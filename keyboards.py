from aiogram import types
def start_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=True)
    btn = types.KeyboardButton("Создать новый плей-лист")
    markup.add(btn)
    return markup

def user_all_pl_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=True)
    btn = types.KeyboardButton("Мои плей-листы")
    markup.add(btn)
    return markup
def user_pl_lists(coll):
    if coll is False:
        return coll
    else:
        markup = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=True)
        for i in coll:
            markup.add(types.InlineKeyboardButton(f"{i}", callback_data=f"plist_{i}"))
        return markup


def playlist_inline_k(plist):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=True)
    btn1 = types.InlineKeyboardButton("Слушать", callback_data=f"listen_{plist}")
    btn2 = types.InlineKeyboardButton("Добавить песню", callback_data=f"add_{plist}")
    btn3 = types.InlineKeyboardButton("Удалить песню", callback_data=f"delsong_{plist}")
    btn4 = types.InlineKeyboardButton("Удалить плей-лист", callback_data=f"dellist_{plist}")
    markup.add(btn1,btn2,btn3,btn4)
    return markup
def playlist_inline_k2(plist):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=True)
    btn2 = types.InlineKeyboardButton("Добавить песню", callback_data=f"add_{plist}")
    btn4 = types.InlineKeyboardButton("Удалить плей-лист", callback_data=f"dellist_{plist}")
    markup.add(btn2,btn4)
    return markup
def add_song_k(pln,name):
    if pln is False:
        return pln
    else:
        markup = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=True)
        for i in pln:
            markup.add(types.InlineKeyboardButton(f"Добавить в {i}", callback_data=f"sadd_{i}_{name}"))
        return markup

def del_all_in_chat():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=True)
    btn = types.KeyboardButton("Удалить все песни в чате")
    markup.add(btn)
    return markup
def delS(songs,pln):
    if songs is False:
        return songs
    else:
        markup = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=True)
        for i in songs:
            markup.add(types.InlineKeyboardButton(f"{i}", callback_data=f"del_{i}_{pln}"))
        return markup

