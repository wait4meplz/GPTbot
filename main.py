import vk_api
import openai
import tokss
import sqlitebase
import aiohttp
import asyncio
from vkbottle.user import User
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import CommandRule, RegexRule
from vkbottle import API, BaseStateGroup, CtxStorage

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard,VkKeyboardColor

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime



openai.api_key = tokss.AItoken
vk_session = vk_api.VkApi(token = tokss.VKtoken)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


vk_sessionbot = vk_api.VkApi(token = tokss.VKtoken)
session_apibot = vk_session.get_api()
longpollbot = VkBotLongPoll(vk_session,218079348)

infsql = sqlitebase.botBD()

def botai(user_id,msg,keyboard):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=msg,
      #temperature=0.9,
      max_tokens=500,
      top_p=1,
      #frequency_penalty=0.0,
      #presence_penalty=0.6,
      #stop=[" Human:", " AI:"]
    )
    return vk_session.method('messages.send',{'user_id':user_id, 'message':response['choices'][0]['text'],'keyboard': keyboard.get_keyboard(),'random_id':0})
    #print(response['choices'][0]['text'])

def get_picture(user_id, msg,keyboard):

    response = openai.Image.create(
        prompt = msg,
        n = 1,
        size="256x256"
    )
    return vk_session.method('messages.send', {'user_id': user_id, 'message': response['data'][0]['url'],'keyboard': keyboard.get_keyboard(), 'random_id': 0})



def sender(user_id, text):
    return vk_session.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': 0})
print(longpoll,vk_session)

infsql.trysql2()

keyboard = VkKeyboard()
keyboard.add_callback_button('нарисуй', VkKeyboardColor.PRIMARY, {"cmd": "click"})
keyboard.add_callback_button('id', VkKeyboardColor.PRIMARY, {"cmd": "click3"})
msg=""
for event in VkBotLongPoll(vk_session,218079348).listen():

    print(event.object.event_id,event.object.user_id,event.object.peer_id)

    if event.type == VkBotEventType.MESSAGE_EVENT:

        event_id = event.object.event_id
        user_id = event.object.user_id
        peer_id = event.object.peer_id

        print(event.object.payload, event.object.payload.get('cmd'),msg)
        if event.object.payload.get('cmd') == 'click' and msg != "":

            get_picture(user_id, msg, keyboard)

        vk_session.method('messages.sendMessageEventAnswer',{'event_id': event_id, 'peer_id': peer_id, 'user_id': user_id, 'random_id': 0})

    elif event.type == VkBotEventType.MESSAGE_NEW: #and event.to_me 'peer_id':peer_id,

        msg = event.object.message['text']
        user_id = event.object.message['from_id']
        print(msg, user_id, event.type)
        print(msg,user_id,event.object)

        if msg != "":
            print(msg + "2")
            botai(user_id, msg, keyboard)
