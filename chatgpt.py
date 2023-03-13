import os
import openai
from telegram.ext import Updater
import requests
from bs4 import BeautifulSoup
from telegram.ext import MessageHandler, Filters
import re


TOKEN = "YOUR TOKEN"
API_KEY = "YOUR API_KEY"
#bot : img_ai_2023_bot
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY
# model = ""

def img_maker(prompt):
    response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
    image_url = response['data'][0]['url']
    print(image_url)
    return image_url

def text_completer(prompt):
    response = openai.Completion.create(\
    model="text-davinci-003",\
    prompt=prompt,\
    temperature=0.4,\
    max_tokens=4000,\
    top_p=1,\
    frequency_penalty=0,\
    presence_penalty=0\
    )
    text = response['choices'][0]['text']
    return text

def code_maker(prompt):
    response = openai.Completion.create(model="code-davinci-002",\
    prompt=prompt,\
    temperature=0,\
    max_tokens=4000,\
    top_p=1.0,\
    frequency_penalty=1.0,\
    presence_penalty=0.0,\
    stop=["\"\"\""])
    code = response['choices'][0]['text']
    return code

def trash_remover(target):
    p = re.compile('[+]')
    cleaned = p.sub('', target)
    return cleaned

def converter(code):
    pass

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def echo(update, context):
    user_id = update.effective_chat.id
    user_text = update.message.text
    user_text = user_text.split()
    
    if user_text[0] == '/aim' or user_text[0] == '/그림'  or user_text[0] == '/pic':
        final_text = ""
        
        for i in range(1, len(user_text)):
            final_text += user_text[i] + " "
            print(final_text)
        text = img_maker(final_text)
        context.bot.send_message(chat_id=user_id, text=text)
    elif user_text[0] == '/code':
        final_text = ""
        
        for i in range(1, len(user_text)):
            final_text += user_text[i] + " "
            print(final_text)
        try:
            text_temp = trash_remover(code_maker(final_text))
            text = text_temp[:4095]
        except Exception as e:
            text = e
        context.bot.send_message(chat_id=user_id, text=text)
        
    elif user_text[0] == '/txt':
        final_text = ""
        
        for i in range(1, len(user_text)):
            final_text += user_text[i] + " "
            print(final_text)
        text = text_completer(final_text)
        context.bot.send_message(chat_id=user_id, text=text)
        
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling(timeout=3, drop_pending_updates=True)
updater.idle()