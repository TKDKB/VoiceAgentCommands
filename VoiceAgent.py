from datetime import date, datetime

import speech_recognition
import pyttsx3
import re


def say(reply: str):
    engine = pyttsx3.init()
    engine.say(reply)
    engine.runAndWait()


def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        # использование online-распознавания через Google
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит выброс ошибки
        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")

        return recognized_data



def assistant():
    time_prompt = ["сколько время", "сколько времени", "время"]
    date_prompt = ["какое сегодня число", "дата"]
    while True:
        voice_input = record_and_recognize_audio()
        recognition_filter(voice_input)
        say(voice_input)
        print(voice_input)
        if voice_input in date_prompt:
            current_date = date.today()
            result = str(current_date.day) + " " + str(current_date.month) + " " + str(current_date.year)
            say(result)
        elif voice_input in time_prompt:
            current_time = datetime.now().time()
            result = str(current_time).split(":")[0] + " " + str(current_time).split(":")[1]
            say(result)
        elif voice_input == "стоп":  # окончание работы по команде "стоп"
            say("до свидания")
            break

def get_nodes_identifiers(data, flag):
    data_list = data.split(' ')
    identifier_1 = []
    identifier_2 = []
    end_words_list = ["до", "к", "в"]
    border = 0
    for end_word in end_words_list:
        if end_word in data_list:
            border = data_list.index(end_word)
            break

    if border:
        for word in data_list[:border]:
            if re.match(r'^[a-zA-Z]+$', word):
                identifier_1.append(word)

        for word in data_list[border:]:
            if re.match(r'^[a-zA-Z]+$', word):
                identifier_2.append(word)

        print(identifier_1)
        print(identifier_2)

    else:
        print("Запрос не соответствует стандартному шаблону")


def recognition_filter(data: str):
    if "построить дугу" in data:
        get_nodes_identifiers(data,True)
    elif "удалить дугу" in data:
        get_nodes_identifiers(data,False)


if __name__ == "__main__":
    # create_edge_pattern = "Построй дугу из 'identifier' в 'identifier'"

    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    assistant()
