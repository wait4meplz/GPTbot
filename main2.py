import json
import openai
import psycopg2
import tokss
import asyncio

from vkbottle import Keyboard, KeyboardButtonColor,Text,OpenLink,GroupEventType,GroupTypes,Callback
from vkbottle.bot import Bot, Message,MessageEvent
from vkbottle import API, BaseStateGroup, CtxStorage





bot=Bot(tokss.VKtoken)
openai.api_key = tokss.AItoken
msgsql=[]

keyboard = Keyboard()
keyboard.add(Callback('НАРИСУЙ',{'cmd':'click'}),color=KeyboardButtonColor.POSITIVE)
keyboard.add(Callback('Сброс памяти', {'cmd': 'click2'}), color=KeyboardButtonColor.NEGATIVE)
keyboard.row()
keyboard.add(Callback('Точный ответ', {'cmd': 'click3'}), color=KeyboardButtonColor.PRIMARY)
keyboard.add(Callback('ChatBot', {'cmd': 'click4'}), color=KeyboardButtonColor.SECONDARY)


def resetchat(user_id):
    connect = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='1',
        database='forbot'
    )

    with connect.cursor() as cursor:
        cursor.execute(f'''DELETE FROM dialogs WHERE user_id = {user_id};''')
        cursor.execute(f'commit;')


def botai(msg):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=msg,
      temperature=0.9,
      max_tokens=2048,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.6,
      stop=[" Human:", " AI:"]
    )
    return response['choices'][0]['text']

def get_picture(msg):

    response = openai.Image.create(
        prompt = msg,
        n = 1,
        size="256x256"
    )
    return response['data'][0]['url']

def get_chat(msg):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = msg,
        max_tokens=512
    )
    return response['choices'][0]['message']['content']





class MenuState(BaseStateGroup):
    PICTURE = 'picture'
    RESET = 'reset'
    ANSWER = 'answer'
    CHAT = 'chat'

def get_id(user_id):
    connect = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='1',
        database='forbot'
    )
    with connect.cursor() as cursor:
        cursor.execute(f'''select user_id from users where user_id = {user_id};''')
        tagfound = cursor.fetchone()
        print(tagfound,user_id)

        if tagfound == None:
            cursor.execute(f'''insert into users (user_id, namefirst, namesecond) values ('{user_id}','KATY','PIDOR');''')
            cursor.execute(f'commit;')

    connect.close()

def msgtable(user_id,msg):
    connect = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='1',
        database='forbot'
    )

    with connect.cursor() as cursor:
        cursor.execute(f'''insert into dialogs (user_id, msg) values ('{user_id}','{msg}');''')
        cursor.execute(f'commit;')
        cursor.execute(f'''select msg from dialogs where user_id = '{user_id}';''')
        tagfound = cursor.fetchall()
        print(tagfound)
        for i in tagfound:
            print(i[0],msgsql)
            msgsql.append({'role': 'user', 'content': str(i[0])})
        connect.close()

    return msgsql


@bot.on.message(state = None)
async def message_handler(message:Message):
    get_id(message.from_id)
    await message.answer('Выбери один из режимов',keyboard=keyboard)


@bot.on.raw_event(GroupEventType.MESSAGE_EVENT,dataclass=GroupTypes.MessageEvent)
async def message_event_handler(event:GroupTypes.GroupJoin):
    if event.object.payload['cmd']=='click':
        await bot.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=json.dumps({'type': 'show_snackbar', 'text': 'режим Рисования'})
        )
        await bot.state_dispenser.set(event.object.peer_id, MenuState.PICTURE)
    elif event.object.payload['cmd']=='click2':
        resetchat(event.object.user_id)
        await bot.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=json.dumps({'type': 'show_snackbar', 'text': 'Бот сброшен...'})
        )
        await bot.state_dispenser.set(event.object.peer_id, MenuState.RESET)
    elif event.object.payload['cmd']=='click3':
        await bot.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=json.dumps({'type': 'show_snackbar', 'text': 'режим Точный ответ'}))
        await bot.state_dispenser.set(event.object.peer_id, MenuState.ANSWER)
    elif event.object.payload['cmd'] == 'click4':
        await bot.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=json.dumps({'type': 'show_snackbar', 'text': 'режим ChatBOT'}))
        await bot.state_dispenser.set(event.object.peer_id, MenuState.CHAT)



@bot.on.message(state=MenuState.PICTURE)
async def picture(event:(Message,GroupTypes.GroupJoin)):
    print(event.payload,type(event.payload))
    ans=get_picture(event.text)
    await event.answer(ans, keyboard=keyboard)



@bot.on.message(state=MenuState.RESET)
async def bot_reset(event:(Message,GroupTypes.GroupJoin)):
    print(event.payload,type(event.payload))
    await event.answer('вы в режиме RESET BOT, переключите режим', keyboard=keyboard)



@bot.on.message(state=MenuState.ANSWER)
async def bot_ai(event:(Message,GroupTypes.GroupJoin)):
    print(event.payload,type(event.payload))
    ans=botai(event.text)
    await event.answer(ans, keyboard=keyboard)



@bot.on.message(state=MenuState.CHAT)
async def bot_chat(event:(Message,GroupTypes.GroupJoin)):
    print(event.payload,type(event.payload))
    msgtable(event.from_id,event.text)
    ans = get_chat(msgsql)
    await event.answer(ans, keyboard=keyboard)

bot.run_forever()