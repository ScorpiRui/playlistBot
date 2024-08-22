import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import keyboards
from bot_base import creat_user_table
from bot_base import creat_users_pl_table
import bot_base
logging.basicConfig(level=logging.INFO)
TOKEN = '5107750827:AAHyD1nDBgykWrNrtPzCHY8_DGANtPgj6Jo'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
class Users:
    def __init__(self, id, user_name):
        self.id = id
        self.user_name = user_name
@dp.message_handler(commands=["start"])
async def sendHello(message: types.Message):
    u = Users(f'{message.chat.id}',f'{message.from_user.username}')
    if creat_user_table(u):
        await bot.send_message(message.chat.id, "Привет если хочешь слушать музыку создай свой плей-лист" , reply_markup=keyboards.start_keyboard())
    else:
        try:
            if bot_base.user_lists(message.from_user.id):
                await bot.send_message(message.chat.id, 'Ваши плей листы', reply_markup=keyboards.user_pl_lists(bot_base.user_lists(message.from_user.id)))
            else:await bot.send_message(message.chat.id, "Привет если хочешь слушать музыку создай свой плей-лист" , reply_markup=keyboards.start_keyboard())
        except:await bot.send_message(message.chat.id, "Привет если хочешь слушать музыку создай свой плей-лист" , reply_markup=keyboards.start_keyboard())
@dp.message_handler(text=['Создать новый плей-лист'])
async def newPl(message: types.Message):
    await bot.send_message(message.chat.id, "Напишите названия вашего плей-листа и в конце напишите слова 'add' его для потверждения.Например \n Плейлист №1 add")



@dp.message_handler(content_types='audio')
async def add_song(message:types.Message):
    arr = ['&','$','@','^','*','_']
    fl = ""
    for i in arr:
        if i in message.audio.file_name:
            fl = ' '.join(message.audio.file_name.split(f"{i}"))
        else:
            fl = ' '.join(message.audio.file_name.split())
    await bot.delete_message(message.chat.id, message.message_id)
    try:
        if bot_base.user_lists(message.chat.id):
            await message.answer(f"{fl.split('.m')[0]}\nВыберите плей лист", reply_markup=keyboards.add_song_k(bot_base.user_lists(message.chat.id),fl.split('.mp')[0]))

        else:await message.answer("У вас нет плей листов",reply_markup=keyboards.start_keyboard())
    except:await message.answer("У вас нет плей листов",reply_markup=keyboards.start_keyboard())
    else:bot_base.songs(message.chat.id,fl,message.audio.file_id)
@dp.message_handler(text="Удалить все песни в чате")
async def reTrue(m:types.Message):
    var = bot_base.delChat(m.chat.id)
    if var:
        for i in var:
            await bot.delete_message(m.chat.id,i)
        await bot.send_message(m.chat.id, "Все песни удалены из чата",reply_markup=keyboards.user_all_pl_keyboard())
    else:await bot.send_message(m.chat.id,"Все песни удалены из чата",reply_markup=keyboards.user_all_pl_keyboard())
@dp.message_handler(text='Мои плей-листы')
async def s_u_pl(message: types.Message):
    if bot_base.user_lists(message.from_user.id):
        try:
            await bot.send_message(message.chat.id, "Ваши плей лиcты", reply_markup=keyboards.user_pl_lists(bot_base.user_lists(message.from_user.id)))
        except:await bot.send_message(message.chat.id, "У вас нет плей листов",reply_markup=keyboards.start_keyboard())
    else:await bot.send_message(message.chat.id, "У вас нет плей листов",reply_markup=keyboards.start_keyboard())
@dp.message_handler(content_types=['text'])
async def addPl(message: types.Message):
    if "_" in message.text.strip():
        await bot.send_message(message.chat.id,'У вас уже есть плей-лист с таким названием  или нельзя создать плей-лист с таким названием')
    else:
        if message.text.strip().endswith('add'):
             if creat_users_pl_table(message.chat.id,message.text[:-4]):
                await bot.send_message(message.chat.id, "Ваш плей лист создан", reply_markup=keyboards.user_all_pl_keyboard())
             else:
                await bot.send_message(message.chat.id, 'У вас уже есть плей-лист с таким названием или нельзя создать плей-лист с таким названием')
        else:
            await bot.send_message(message.chat.id, "Если хотите открыть плей-лист с этим названиям добавте слова 'add' в конце названия")

@dp.callback_query_handler(Text(startswith='plist'))
async def caller(call:types.CallbackQuery):
    pln= call.data.split("_")[1]
    songs = bot_base.get_list_song(call.from_user.id,pln)
    res = ""
    if songs:
        for i in songs:
           res+=f'{i}\n'
        await call.message.answer(f"{pln}\n{res}", reply_markup=keyboards.playlist_inline_k(pln))
        await call.answer()
    else:
        await call.message.answer(f"{pln}\n Этот плей лист пуст", reply_markup=keyboards.playlist_inline_k2(pln))
        await call.answer()
@dp.callback_query_handler(Text(startswith='sadd_'))
async def adder(call:types.CallbackQuery):
    pln= call.data.split("_")[1]
    name = call.data.split("_")[2]
    songdata = bot_base.last_song(call.from_user.id, name)
    if songdata:
        song_id = songdata
        if bot_base.insert_song_into_list(call.from_user.id,pln,name,song_id):
            await call.answer("Песня добавлена в плей лист")
        else:await call.answer("Это песня уже эсть в этом плей-листе или произошла ошибка",show_alert=True)
    else:await call.answer("Это песня уже эсть в этом плей-листе или произошла ошибка",show_alert=True)

@dp.callback_query_handler(Text(startswith='add'))
async def forlisten(call:types.CallbackQuery):
    await call.message.answer("Отпавте файл '.MP3' который хотите добавить ")
    await call.answer()


@dp.callback_query_handler(Text(startswith='listen_'))
async def listen(call: types.CallbackQuery):
    pln= call.data.split("_")[1]
    try:
        songs = bot_base.listenTo(call.from_user.id,pln)
        for i in songs:
           me = await call.message.answer_audio(f'{i}',reply_markup=keyboards.del_all_in_chat())
           bot_base.chat(call.from_user.id,me.message_id)
           await call.answer()
    except:
        await call.message.answer(f"Этот плей лист пуст", reply_markup=keyboards.playlist_inline_k2(pln))
        await call.answer()
@dp.callback_query_handler(Text(startswith='delsong_'))
async def delCh(call: types.CallbackQuery):
    pln = call.data.split('_')[1]
    try:
        await call.message.answer(f'Выберите песню которую хотите удалить в {pln}',reply_markup=keyboards.delS(bot_base.get_list_song(call.from_user.id,pln),pln))
        await call.answer()
    except:await call.answer(f"ОШИБКА")

@dp.callback_query_handler(Text(startswith='del_'))
async def delSong(call:types.CallbackQuery):
    song = call.data.split('_')[1]
    pln = call.data.split('_')[2]
    if bot_base.delSong(call.from_user.id,pln,song):
        await call.answer("Песня удалена")
    else:
        await call.answer("ОШИБКА")

@dp.callback_query_handler(Text(startswith='dellist_'))
async def delPl(call:types.CallbackQuery):
    pln = call.data.split('_')[1]
    if bot_base.delList(call.from_user.id,pln):
        await call.message.answer("Плей-лист удалён", reply_markup=keyboards.user_all_pl_keyboard())
        await call.answer()
    else:
        await call.answer("ОШИБКА")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

