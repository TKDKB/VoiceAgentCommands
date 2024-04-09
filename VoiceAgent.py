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


def get_nodes_identifiers(data):
    data_list = data.split(' ')
    identifier_1 = []
    identifier_2 = []
    end_words_list = ["до", "к", "в"]
    for end_word in end_words_list:
        if end_word in data_list:
            border = data_list.index(end_word)
            break

    for word in data_list[:border]:
        if re.match(r'^[a-zA-Z]+$', word):
            identifier_1.append(word)

    for word in data_list[border:]:
        if re.match(r'^[a-zA-Z]+$', word):
            identifier_2.append(word)

    print(identifier_1)
    print(identifier_2)


def recognition_filter(data: str):
    if "построй дугу" in data:
        get_nodes_identifiers(data)


if __name__ == "__main__":
    create_edge_pattern = "Построй дугу из 'identifier' в 'identifier'"

    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    data = record_and_recognize_audio()
    recognition_filter(data)

    print(data)
    say(data)
