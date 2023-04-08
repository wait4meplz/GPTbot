import asyncio
from vkbottle.user import User
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import CommandRule, RegexRule
from vkbottle import API, BaseStateGroup, CtxStorage
from settings import myApi,groupApi, comms, helpmes, dialogHelp
import numpy as np
import os
import sys
import requests
import urllib.request

from copilot import Copilot

ctx = CtxStorage()

class States(BaseStateGroup):
    GENERATING = 0
    DIALOG_CH = 1
    DIALOG = 2
    END = 3

class StatesPicture(BaseStateGroup):
    Q = 0
    END = 1

dialog = np.load('/GPTbot/second/dialogs.npy', allow_pickle='True').item()

bot = Bot(token=groupApi)
user = User(token=myApi)
api = API(token=groupApi)
myApi = API(token=myApi)

def _generate_copilot(prompt: str):
    copilot = Copilot()
    c = copilot.get_answer(prompt  )

    return c

def _generate_picture(prompt: str):
    copilot = Copilot()
    c = copilot.get_picture(prompt)

    return c

def _generate_dialog(prompt):
    copilot = Copilot()
    c = copilot.get_dialog(prompt)

    return c

@bot.on.private_message(state=None)
async def messageHandler(message: Message):
    text = message.text
    if '/ответ' in text:
        await message.answer('✅ Генерирую ответ...')
        answer = await generateAnswer(message.from_id, text.replace('/ответ', ""))
        await message.answer(answer)
    elif '/точныйответ' in text:
        await message.answer('✅ Генерирую ответ... (точный ответ теперь можно получить командой /ответ)')
        answer = await generateAnswer(message.from_id, text.replace('/ответ', ""))
        await message.answer(answer)
    elif '/картинка' in text:
        await message.answer(
            '✅ Генерирую картинку... (30 секунд - 5 минут, всё зависит от загруженности бота, если дольше - напиши запрос заново)')
        answer = await generatePicture(message.from_id, text.replace('/ответ', ""))
        await message.answer(answer)
    elif '/диалог' in text:
        await generateDialog(message)
    elif text == '/отмена':
        await bot.state_dispenser.set(message.peer_id, States.END)
        await message.answer('✅ Сбросил всю информацию.')
    elif text.lower() == 'команды' or text.lower() == 'помощь':
        await message.answer(helpmes)
    elif text.split(" ")[0] == 'бот':
        if text.split(" ")[1] == 'перезагрузись':
            await message.answer('Скоро буду...')
            os.system('python3 bot.py')
            sys.exit(0)
        if text.split(" ")[1] == 'выключись':
            await message.answer('Пока!')
            os.system('python3 wait.py')
            sys.exit(0)
        elif text.split(" ")[1] == 'тут':
            await message.answer('Тут!')
    elif len(message.attachments) > 0:
        mes = message
        if mes.attachments[0].audio_message.duration > 60:
            await message.answer('❌Слишком большая ГС, извини :(')
        else:
            await mes.answer('💬Читаю голосовую, жди...')
            await asyncio.sleep(5)
            for i in range(3):
                try:
                    bbb = await api.messages.get_history(user_id=message.from_id, count=2, offset=1)
                except Exception as e:
                    await mes.answer(f'❌ Не удалось, попытка {i}... \n Причина ошибки: {e}')
                else:
                    if bbb.items[0].attachments[0].audio_message.transcript_state == 'done':
                        ts = bbb.items[0].attachments[0].audio_message.transcript
                        await bot.state_dispenser.set(message.from_id, States.GENERATING)
                        answer = _generate_copilot(ts)
                        await message.answer(f'💬 Ты спросил "{ts}", бот ответил:\n\n' + answer)
                        break
                    else:
                        continue

    else:
        await message.answer('Привет! Чтобы узнать список команд, напиши "команды"! :з')

@bot.on.private_message(state=States.END)
async def messageHandler2(message: Message):
    text = message.text
    if '/ответ' in text:
        await message.answer('✅ Генерирую ответ...')
        answer = await generateAnswer(message.from_id, text.replace('/ответ', ""))
        await message.answer(answer)
    elif '/точныйответ' in text:
        await message.answer('✅ Генерирую ответ... (точный ответ теперь можно получить командой /ответ)')
        answer = await generateAnswer(message.from_id, text.replace('/ответ', ""))
        await message.answer(answer)
    elif '/картинка' in text:
        await message.answer(
            '✅ Генерирую картинку... (30 секунд - 5 минут, всё зависит от загруженности бота, если дольше - напиши запрос заново)')
        answer = await generatePicture(message.from_id, text.replace('/ответ', ""))
        await message.answer(answer)
    elif '/диалог' in text:
        await generateDialog(message)
    elif text == '/отмена':
        await bot.state_dispenser.set(message.peer_id, States.END)
        await message.answer('✅ Сбросил всю информацию.')
    elif text.lower() == 'команды' or text.lower() == 'помощь':
        await message.answer(helpmes)
    elif text.split(" ")[0] == 'бот':
        if text.split(" ")[1] == 'перезагрузись':
            await message.answer('Скоро буду...')
            os.system('python3 bot.py')
            sys.exit(0)
        if text.split(" ")[1] == 'выключись':
            await message.answer('Пока!')
            os.system('python3 wait.py')
            sys.exit(0)
        elif text.split(" ")[1] == 'тут':
            await message.answer('Тут!')
    elif len(message.attachments) > 0:
        mes = message
        if mes.attachments[0].audio_message.duration > 60:
            await message.answer('❌Слишком большая ГС, извини :(')
        else:
            await mes.answer('⌛ Читаю голосовую, жди...')
            await asyncio.sleep(5)
            for i in range(3):
                try:
                    bbb = await api.messages.get_history(user_id=message.from_id, count=2, offset=1)
                except Exception as e:
                    await mes.answer(f'❌ Не удалось, попытка {i}... \n Причина ошибки: {e}')
                else:
                    if bbb.items[0].attachments[0].audio_message.transcript_state == 'done':
                        ts = bbb.items[0].attachments[0].audio_message.transcript
                        await bot.state_dispenser.set(message.from_id, States.GENERATING)
                        answer = _generate_copilot(ts)
                        await message.answer(f'💬 Ты спросил "{ts}", бот ответил:\n\n' + answer)
                        break
                    else:
                        continue

    else:
        await message.answer('Привет! Чтобы узнать список команд, напиши "команды"! :з')


@bot.on.private_message(text=('сгенерируй','сгенерировать','Сгенерируй','Сгенерировать'), state=States.END)
async def start(message: Message):
    await bot.state_dispenser.set(message.peer_id, States.END)
    await message.answer('⚠ Привет, я поменял бота. Теперь он по командам: \n\n /ответ <запрос> \n/картинка <запрос>\n/диалог\nЛибо введи "команды"')

async def generatePicture(peerid, prompt):
    await bot.state_dispenser.set(peerid, States.END)
    await bot.state_dispenser.set(peerid, States.GENERATING)
    answer = _generate_picture(prompt)
    await bot.state_dispenser.set(peerid, States.END)
    return ('Ссылка на картинку: ' + answer)

async def generateAnswer(peerid, msg):
    await bot.state_dispenser.set(peerid, States.END)
    await bot.state_dispenser.set(peerid, States.GENERATING)
    answer = _generate_copilot(msg)
    await bot.state_dispenser.set(peerid, States.END)
    return answer

async def generateDialog(message):
    await bot.state_dispenser.set(message.peer_id, States.END)
    await message.answer(dialogHelp)
    await bot.state_dispenser.set(message.peer_id, States.DIALOG_CH)

@bot.on.private_message(state=States.DIALOG_CH)
async def generateDialog2(message: Message):
    if len(message.text.split()) < 10:
        await message.answer('⚠ Характер бота задан, теперь можешь общаться с ним :)\n\nЧтобы выйти из режима диалога, напиши /отмена.Чтобы сбросить характер, напиши /сброс.  \n\n(бот обнаружил, что ты задал довольно короткое описание характера. Если тебе не подойдёт текущий - напиши характер ещё раз поподробнее.)')
    else:
        await message.answer(
            '💬 Характер бота задан, теперь можешь общаться с ним :)\n\nЧтобы выйти из режима диалога, напиши /отмена. Чтобы сбросить характер, напиши /сброс')
    dialog[message.from_id] = [{'role': 'system', 'content': f'{message.text}'}]
    await bot.state_dispenser.set(message.peer_id, States.DIALOG)

@bot.on.private_message(state=States.DIALOG, text='/сброс')
async def dialogStop(message: Message):
    await bot.state_dispenser.set(message.peer_id, States.END)
    dialog.pop(message.from_id)
    await bot.state_dispenser.set(message.peer_id, States.DIALOG_CH)
    await message.answer('✅ Окей, сбросил диалог. Напиши новый характер собеседника!')

@bot.on.private_message(state=States.DIALOG, text='/отмена')
async def dialogStop(message: Message):
    await bot.state_dispenser.set(message.peer_id, States.END)
    dialog.pop(message.from_id)
    await message.answer('✅ Вышел из режима диалога.')

@bot.on.private_message(text='/отмена')
async def dialogStop(message: Message):
    await bot.state_dispenser.set(message.peer_id, States.END)
    await message.answer('✅ Вышел из режима диалога.')

@bot.on.private_message(state=States.DIALOG)
async def dialogGenerate(message: Message):
    await message.answer('⏳ Генерирую ответ...')
    if message.text in comms:
        dialog[message.from_id].append({'role' : 'user', 'content' : message.text})
        answer = _generate_dialog(dialog[message.from_id])
        await message.answer(answer[0] + "\n\n(⚠если хочешь выйти из диалога - напиши /отмена⚠)")
    elif len(message.attachments) > 0:
        await message.answer('❌ Бот не может просматривать вложения (в том числе голосовые) в режиме диалога.')
    else:
        dialog[message.from_id].append({'role': 'user', 'content': message.text})
        answer = _generate_dialog(dialog[message.from_id])
        await message.answer(answer[0])

@bot.on.private_message(state=States.GENERATING)
async def alreadyGenerating(message: Message):
    await message.answer('⚠Ты уже генерируешь запрос! Дождись окончания.')

@bot.on.private_message(text='дебаг <msg>')
async def deb(message: Message, msg):
    text = message.text.lower()
    text2 = message.text.split(" ")
    if msg == 'доны':
        a = await myApi.donut.get_subscription(owner_id=-219131806)
        print(a)

@bot.on.private_message(text='бот <msg>')
async def reload(message: Message, msg):
    if msg == 'перезагрузись':
        await message.answer('Скоро буду...')
        os.system('python3 bot.py')
        sys.exit(0)
    if msg == 'выключись':
        await message.answer('Пока!')
        os.system('python3 wait.py')
        sys.exit(0)
    elif msg == 'тут':
        await message.answer('Тут!')
bot.run_forever()