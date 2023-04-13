import speech_recognition as sr

from selenium import webdriver
import keyboard

from googletrans import Translator

import requests
import re
def listen():
    voice_recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Слушаю >>> ")
        audio = voice_recognizer.listen(source)

    try:
        voice_text = voice_recognizer.recognize_google(audio, language="ru")
        print(f"Вы сказали: {voice_text}")
        return voice_text
    except sr.UnknownValueError:
        return "ошибка распознания"
    except sr.RequestError:
        return "ошибка запроса"


def say(text):
    # voice = gTTS(text, lang="ru")
    # unique_file = "audio_" + str(random.randint(0, 10000)) + ".mp3"  # audio_10.mp3
    # voice.save(unique_file)
    #
    # playsound.playsound(unique_file)
    # os.remove(unique_file)
    print(f"Ассистент: {text}")


def handle_command(command):
    command = command.lower()
    if command == "привет":
        say("Привет-привет")
    elif command == "стоп":
        stop()
    elif command in "заметка":
        readFile()
    elif command in "узнать заметку":
        openZametki()
    elif command in "найди видео":
        findYT()
    elif command in "переведи слово":
        translateWord()
    elif command in "погода":
        weather()
    else:
        say("Не понятно, повторите")


def stop():
    say("Счастливо, в попе слива!")
    exit()


def start():
    print("Запуск ассистента...")

    while True:
        command = listen()
        handle_command(command)

def readFile():
    print('Скажите название заметки')
    nameZametki = listen()
    file = open('C:\\Users\\amir1\\PycharmProjects\\skillbox-voice-assistant\\app\\'+nameZametki+'.txt', 'w', encoding="utf8")
    print('Что записать?')
    message = listen()
    print(file.write(message))
    file.close()

def openZametki():
    print('Какую заметку открыть?')
    message = listen()
    file = open(message + '.txt', 'r', encoding="utf8")
    print(message + '.txt')
    print(file.read())
    file.close()

def findYT():
    print('Какое видео найти?')
    searchVideo = listen()

    driver = webdriver.Chrome()
    driver.get(f'https://www.youtube.com/results?search_query={searchVideo.replace(" ", "+")}')

    print('Нажмите "Esc", чтобы закрыть браузер.')
    # Listen for key press event
    def on_key_press(event):
        if event.name == 'esc':
            driver.quit()
            keyboard.unhook_all()

    # Hook the key press event
    keyboard.on_press(on_key_press)

    # Wait until the browser window is closed
    keyboard.wait('esc')

def findYandex():
    print('Какое видео найти?')
    user_query = listen()

    blok_list = user_query.split()  # разбиваем слова по пробелам
    url_query = '%20'.join(blok_list)  # разделяем их через %20
    url = 'https://yandex.ru/search/?text=' + url_query + '&lr=213'  # подставляем
    print(url)

    driver = webdriver.Chrome()
    driver.get(url)

    print('Нажмите "Esc", чтобы закрыть браузер.')

    # Listen for key press event
    def on_key_press(event):
        if event.name == 'esc':
            driver.quit()
            keyboard.unhook_all()

    # Hook the key press event
    keyboard.on_press(on_key_press)

    # Wait until the browser window is closed
    keyboard.wait('esc')

# нужно будет добавить вопрос с какого на какой переводить
def translateWord():
    print('Какое слово перевести? ')
    user_word = listen()

    translator = Translator()
    result = translator.translate(user_word, src='ru', dest='en')
    print('Перевод: ' + result.text)

def weather():
    print("Сам скажешь?")
    def nowLocation():
        # Получаем IP-адрес пользователя
        ip_address = requests.get('https://api.ipify.org').text

        # Отправляем GET-запрос на сервис определения геолокации
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')

        # Получаем город из ответа
        return  re.sub('[\W_]+', '',response.json()['city'].lower())


    choosingWayToDetermineLocation = listen()

    if ('сам' == choosingWayToDetermineLocation):
        print("Назовите город")
        translator = Translator()
        city = translator.translate(listen(), src='ru', dest='en')
    else:
        city = nowLocation()
    print(f'Вы находитесь в городе {city}')

    url = 'https://yandex.ru/pogoda/' + city  # подставляем
    print(url)

    driver = webdriver.Chrome()
    driver.get(url)

    print('Нажмите "Esc", чтобы закрыть браузер.')

    # Listen for key press event
    def on_key_press(event):
        if event.name == 'esc':
            driver.quit()
            keyboard.unhook_all()

    # Hook the key press event
    keyboard.on_press(on_key_press)

    # Wait until the browser window is closed
    keyboard.wait('esc')
try:
    start()
except KeyboardInterrupt:
    stop()