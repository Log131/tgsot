from aiogram import Dispatcher,Bot,executor,types

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

import asyncio
import sqlite3
from datetime import datetime, time

token = '6093970106:AAFugNzYa1SL0WTgReF4gHznIwqAF6tSRSY'

bot = Bot(token=token)
dp = Dispatcher(bot=bot)
global tbase, tc
tbase = sqlite3.connect('tes.db')
tc = tbase.cursor()
with tbase:
    tc.execute('CREATE TABLE IF NOT EXISTS wars_(username, user_id PRIMARY KEY, war DEFAULT 0)')







@dp.message_handler(commands=['start'])
async def strsx(msg: types.Message):
    with tbase:
        tc.execute('INSERT OR IGNORE INTO wars_(username, user_id) VALUES(?, ?)', (msg.from_user.username, msg.from_user.id,))

@dp.message_handler(commands=['wars'])
async def warsxd_(msg: types.Message):

    try:
        with tbase:
           s = tc.execute('SELECT * FROM wars_').fetchall()
        for i in s:
            try:
                await bot.send_message(chat_id=msg.chat.id, text=f'Пользователь - @{i[0]} Имеет - {i[2]}/5 Варнов')
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    


@dp.message_handler(commands=['war'])
async def warxd_(msg: types.Message):
    try:
        
        chat_admins = await bot.get_chat_member(chat_id='@OwnerOtziv', user_id=msg.from_user.id)
        
        
        
        
        
        
        
        if chat_admins.status == 'creator' or chat_admins.status == 'administrator':
            with tbase:
                s_ = tc.execute('SELECT war FROM wars_ WHERE user_id = ?', (msg.reply_to_message.from_user.id,)).fetchone()
            
            
            
        
            with tbase:
                tc.execute('INSERT OR IGNORE INTO wars_(user_id) VALUES(?)',(msg.reply_to_message.from_user.id,))
            with tbase:
                tc.execute('UPDATE wars_ SET war = war + 1 WHERE user_id = ?',(msg.reply_to_message.from_user.id,))
            with tbase:
                s = tc.execute('SELECT war FROM wars_ WHERE user_id = ?', (msg.reply_to_message.from_user.id,)).fetchone()
            await bot.send_message(msg.reply_to_message.from_user.id, text=f'Вы получили предупреждение ‼️ ‼️ ‼️ {s[0]}/5')
            await bot.send_message(msg.chat.id, text=f'@{msg.reply_to_message.from_user.username}        Вы получили предупреждение ‼️ ‼️ ‼️{s[0]}/5')
            if s_[0] >= 5:
                with tbase:
                    tc.execute('UPDATE wars_ SET war = 0 WHERE user_id = ?', (msg.reply_to_message.from_user.id,))
                await bot.send_message(msg.reply_to_message.from_user.id, text=f'Вы были удалены из чата')
                await bot.send_photo(msg.chat.id, photo='https://i.yapx.ru/V9rL7.png',caption=f'@{msg.reply_to_message.from_user.username} Был отправлен в ЧВК Шелби 🫡')
                await bot.ban_chat_member(msg.chat.id, user_id=msg.reply_to_message.from_user.id)
        else:

            pass
    
    except Exception as e:
        print(e)








@dp.message_handler(commands=['card'])
async def cardxd_(msg: types.Message):
    await msg.answer('_Реквизиты Отзывничка_ : \n 🏦 Тинькофф Банк \n 💳 5536914054972405 \n \n 🏦 Сбербанк \n 💳 2202203293150142 \n \n 📲 +79106265792 (Для переводов по номеру, актуальны только те банки, которые указаны выше ☝️ \n \n🤖 💳Савушкин С.В.', parse_mode='Markdown')



@dp.message_handler(commands=['del'])
async def delxd_(msg: types.Message):
    
    
    
    try:
        chat_admins = await bot.get_chat_member(chat_id='@OwnerOtziv', user_id=msg.from_user.id)
        if chat_admins.status == 'creator' or chat_admins.status == 'administrator':
            s = msg.reply_to_message.from_user.username
            with tbase:
                tc.execute('UPDATE wars_ SET war = war - 1 WHERE user_id = ?', (msg.reply_to_message.from_user.id,))
                s_ = tc.execute('SELECT war FROM wars_ WHERE user_id = ? ',(msg.reply_to_message.from_user.id,)).fetchone()
            

            await bot.send_message(msg.chat.id, text=f'@{s} Предупреждения сняты {s_[0]}/5')
    except:
        pass





async def sends_():

    time_now = datetime.now().time()
    time_ = time(hour=10, minute=0)
    if time_ >= time_now:
        await bot.send_message(chat_id='@GenialniyOtzivnikWork', text='🌟Друзья! \n \n Напоминаем, что в СУТКИ можно писать ТОЛЬКО 1 ОТЗЫВ на каждой площадке. \n \n Увы, но если написать БОЛЕЕ ОДНОГО ОТЗЫВА, то велик шанс его удаления, а следовательно, и блокировка вашего аккаунта. \n \n Спасибо за понимание!')





async def starts_():
    while True:
        await sends_()
        await asyncio.sleep(35)






if __name__ == '__main__':
    s = asyncio.get_event_loop()
    s.create_task(starts_())
    executor.start_polling(dp, skip_updates=True)