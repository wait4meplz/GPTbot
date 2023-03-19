import os
import json
import openai

from settings import chatgptApi

class Copilot:
    def get_answer(self, question):
        prompt = question

        openai.api_key = chatgptApi
        try:
            response = openai.Completion.create(
                engine = "text-davinci-003",
                prompt = prompt,
                max_tokens = 1024,
                top_p = 1
            )
        except openai.error.APIError as e:
            print(e)
            return f'❌ Бот не ответил, причина: ошибка API ChatGPT. Кароч пендосы опять что-то там сломали, нужно подождать.'
        except openai.error.ServiceUnavailableError as e:
            print(e)
            return f'❌ Бот не ответил, причина: Сервера ChatGPT не отвечают. Сломаны/обновляются/выключены, нужно подождать.'
        except openai.error.Timeout as e:
            print(e)
            return '❌ Бот не ответил, причина: Задержки на серверах ChatGPT. Попробуй позже.'
        else:
            return response['choices'][0]['text']

    def get_dialog(self, dialog: list):

        openai.api_key = chatgptApi
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=dialog,
                max_tokens=1024
            )
        except openai.error.APIError as e:
            return f'❌ Бот не ответил, причина: ошибка API ChatGPT. Кароч пендосы опять что-то там сломали, нужно подождать.'
        except openai.error.ServiceUnavailableError as e:
            return f'❌ Бот не ответил, причина: Сервера ChatGPT не отвечают. Сломаны/обновляются/выключены, нужно подождать.'
        except openai.error.Timeout as e:
            return '❌ Бот не ответил, причина: Задержки на серверах ChatGPT. Попробуй позже.'
        else:
            newdialog = dialog.append(response['choices'][0]['message'])
            return response['choices'][0]['message']['content'], newdialog

    def get_picture(self, prompt):
        openai.api_key = chatgptApi
        try:
            response = openai.Image.create(
                prompt = prompt,
                n = 1,
                size="1024x1024"
            )
        except openai.error.InvalidRequestError as e:
            return '❌ Запрос содержит что-то запрещенное. Увы, ChatGPT не позволяет генерировать 18+ или оскорбительные картинки :('
        except openai.error.APIError as e:
            return f'❌ Бот не ответил, причина: ошибка API ChatGPT. Кароч пендосы опять что-то там сломали, нужно подождать.'
        except openai.error.ServiceUnavailableError as e:
            return f'❌ Бот не ответил, причина: Сервера ChatGPT не отвечают. Сломаны/обновляются/выключены, нужно подождать.'
        except openai.error.Timeout as e:
            return '❌ Бот не ответил, причина: Задержки на серверах ChatGPT. Попробуй позже.'
        else:
            return response['data'][0]['url']