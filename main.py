import threading
from random import randint
import telebot
import demapi
from os import environ as env
import Data

API_KEY = env.get('API_KEY')
bot = telebot.TeleBot(API_KEY)

lock = threading.Lock()
db = Data.Data("./database.sqlite")


@bot.message_handler(content_types=['photo'])
def photo_worker(message):
    if message.caption:
        if message.caption[0] == '/' and message.caption[1] == 'd':
            conf = demapi.Configure(
                base_photo=bot.download_file(bot.get_file(message.photo[len(message.photo) - 1].file_id).file_path),
                title=message.caption.partition('d')[2][1:]
            )
            bot.send_photo(message.chat.id, conf.download().content, reply_to_message_id=message.message_id)

    elif randint(1, 100) >= 95:
        lock.acquire(True)
        values_list = [value[1] for value in db.list(message.chat.id)]
        lock.release()

        conf = demapi.Configure(
            base_photo=bot.download_file(bot.get_file(message.photo[len(message.photo) - 1].file_id).file_path),
            title=values_list[randint(0, len(values_list) - 1)]
        )
        bot.send_photo(message.chat.id, conf.download().content, reply_to_message_id=message.message_id)


@bot.message_handler(commands=['add'])
def add_to_list(message):
    # message.from_user.id in bot.get_chat_administrators(message.chat.id)
    status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if status == "administrator" or status == "creator":
        lock.acquire(True)
        phrase_id = db.add(message.chat.id, message.text[5:])
        lock.release()
        if phrase_id != -1:
            bot.send_message(message.chat.id, f"{phrase_id}) '{message.text[5:]}' was added to the list",
                             reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, f"'{message.text[5:]}' already on the list",
                             reply_to_message_id=message.message_id)

    else:
        bot.send_message(message.chat.id, "you do not have enough permissions for this command",
                         reply_to_message_id=message.message_id)


@bot.message_handler(commands=['delete'])
def delete_from_list(message):
    status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if status == "administrator" or status == "creator":

        lock.acquire(True)
        if db.delete(message.chat.id, message.text[8:]):
            bot.send_message(message.chat.id, f"'{message.text[8:]}' was delete from the list",
                             reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, f"'{message.text[8:]}' was not removed from the list",
                             reply_to_message_id=message.message_id)

        lock.release()
    else:
        bot.send_message(message.chat.id, "you do not have enough permissions for this command",
                         reply_to_message_id=message.message_id)


@bot.message_handler(commands=['list'])
def view_list(message):
    lock.acquire(True)
    values_list = db.list(message.chat.id)
    lock.release()

    if len(values_list) == 0:
        bot.send_message(message.chat.id, "list for this chat is empty", reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id, '\n'.join([f"{value[0]}) '{value[1]}'" for value in values_list]),
                         reply_to_message_id=message.message_id)


@bot.message_handler(commands=['edit'])
def edit_phrase(message):
    edit_list = str(message.text).split()
    if len(edit_list) >= 3 and edit_list[1].isdigit():
        lock.acquire(True)
        upd_stat = db.edit(message.chat.id, int(edit_list[1]), ' '.join(edit_list[2:]))
        lock.release()

        if upd_stat:
            bot.send_message(message.chat.id, f"{edit_list[1]} phrase has been changed",
                             reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, f"{edit_list[1]} phrase has not been modified",
                             reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id, "incorrect request format", reply_to_message_id=message.message_id)


if __name__ == "__main__":
    bot.polling(none_stop=True)
