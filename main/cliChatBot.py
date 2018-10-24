from langprocessing import chatbot

print('Hello i am õisBot! Ask me anything. To exit type "!exit".')
bot = chatbot.chatbot()
while 1:
    text = input('>> ')
    if text == '!exit':
        break
    print(bot.getResponse(text))