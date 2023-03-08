from random import randint
import telebot
import demapi
import json
import sys

API_KEY = sys.argv[1]
bot = telebot.TeleBot(API_KEY)

file = open('messages.json', mode='r', encoding='utf-8')
messages = json.load(file)
file.close()


@bot.message_handler(content_types=['photo'])
def photo_worker(message):
    if message.caption:
        if message.caption[0] == '/' and message.caption[1] == 'd':
            conf = demapi.Configure(
                base_photo=bot.download_file(bot.get_file(message.photo[len(message.photo) - 1].file_id).file_path),
                title=message.caption.partition('d')[2][1:]
            )
            bot.send_photo(message.chat.id, conf.download().content, reply_to_message_id=message.message_id)

    elif randint(1, 100) >= 75:
        conf = demapi.Configure(
            base_photo=bot.download_file(bot.get_file(message.photo[len(message.photo) - 1].file_id).file_path),
            title=messages['messages'][randint(0, len(messages['messages']) - 1)]
        )
        bot.send_photo(message.chat.id, conf.download().content, reply_to_message_id=message.message_id)


if __name__ == '__main__':
    bot.polling()
