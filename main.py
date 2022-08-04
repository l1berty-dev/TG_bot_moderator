from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import Database


Channel_URL = "https://t.me/testChannelchatt"
Channel_ID = "@testChannelchatt"
ChatID = "@publicGroupechat"


btnUrlChannel = InlineKeyboardButton('Перейти на канал', url= Channel_URL)
ChannelMenu = InlineKeyboardMarkup(row_width=1)
ChannelMenu.insert(btnUrlChannel)

Words = ["хуй","блять","бля","нахуй","пизда","пизд","мать сдохла","пидорас","мудак","членосос","блядь","сиськи","хуйня",]

AdminID = '700117365'

bot = Bot(token='5539589340:AAHL2qb_jMaBE6YfsAj4A6P0nq6adeAXS8o')
dp = Dispatcher(bot)


db = Database('database.db')

# функция проверки подписки на канал
def check_sub_channel(chat_member):
    return chat_member['status'] != 'left'

@dp.message_handler(content_types=["new_chat_members"])
async def user_joined(message: types.Message):
    await message.answer(f"Добро пожаловать, {message.chat.id}!")

@dp.message_handler(commands=["mute"], commands_prefix='/')
async def mute(message: types.Message):
    if str(message.from_user.id) == AdminID:
        if not message.reply_to_message:
            await message.reply('Эта команда должна быть ответом на сообщение')
            return
        mute_hour = int(message.text[6:])
        db.add_mute(message.reply_to_message.from_user.id, mute_hour)
        await message.bot.delete_message(ChatID, message.message_id)
        await message.reply_to_message.reply(f"Пользователь замучен на {mute_hour} ч.")


@dp.message_handler()
async def mess_handler(message: types.Message):
    # вызов функции проверки на подписку
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    if not db.mute(message.from_user.id):
        if check_sub_channel(await bot.get_chat_member(chat_id=Channel_ID, user_id=message.from_user.id)):
            text = message.text.lower()
            for word in Words:
                if word in text:
                    await message.delete()
        else:
            await message.answer("Что бы отправлять сообщения подпишитесь на канал", reply_markup=ChannelMenu)
            await message.delete()
    else:
        await message.delete()


if __name__ == "__main__":
    executor.start_polling(dp)