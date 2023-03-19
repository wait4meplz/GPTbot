import vk_api
import openai
import tokss
import sqlitebase

import asyncio
from vkbottle.user import User
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import CommandRule, RegexRule
from vkbottle import API, BaseStateGroup, CtxStorage

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard,VkKeyboardColor

from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime



openai.api_key = tokss.AItoken
vk_session = vk_api.VkApi(token = tokss.VKtoken)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


infsql = sqlitebase.botBD()
def botai(user_id,msg,keyboard):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=msg,
      #temperature=0.9,
      max_tokens=150,
      top_p=1,
      #frequency_penalty=0.0,
      #presence_penalty=0.6,
      #stop=[" Human:", " AI:"]
    )
    return vk_session.method('messages.send',{'user_id':user_id, 'message':response['choices'][0]['text'],'keyboard': keyboard.get_keyboard(),'random_id':0})
    #print(response['choices'][0]['text'])

def get_picture(user_id, msg):

    response = openai.Image.create(
        prompt = msg,
        n = 1,
        size="1024x1024"
    )
    return vk_session.method('messages.send', {'user_id': user_id, 'message': response['data'][0]['url'], 'random_id': 0})



def sender(user_id, text):
    return vk_session.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': 0})
print(longpoll,vk_session)

infsql.trysql2()

for event in VkLongPoll(vk_session).listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        user_id = event.user_id



        if msg != "":
            keyboard = VkKeyboard()
            keyboard.add_button('button', VkKeyboardColor.PRIMARY)

            botai(user_id,msg,keyboard)
            get_picture(user_id,msg)



