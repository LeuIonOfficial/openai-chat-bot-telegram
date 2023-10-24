import telebot
import config
import gpt


bot = telebot.TeleBot(config.TOKEN)


user_messages: {int: list} = {}


@bot.message_handler(content_types=["text"])
async def text_handler(message):

    if message.text == "context":
        user_messages[message.chat.id] = []
        bot.send_message(message.chat.id, "context cleared")
    else:
        if message.chat.id in user_messages:
            user_messages[message.chat.id].append({"role": "user", "content": message.text})
        else:
            user_messages[message.chat.id] = [{"role": "user", "content": message.text}]

        response = await gpt.ask(messages=user_messages[message.chat.id])

        user_messages[message.chat.id].append({"role": "assistant", "content": response})

        bot.send_message(message.chat.id, response)
    print(user_messages)


bot.polling(none_stop=True)
