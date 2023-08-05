import speech_recognition as sr
from gtts import gTTS
from playsound import playsound


def speech_to_text(language='ru-RU') -> str:
    """
    This function uses SpeechRecognition library to convert user's speech to text in Russian language.
    It initializes a Recognizer object and a Microphone object to capture the audio. Then, it waits for user's speech input.
    If the speech is successfully recognised, it returns the text. If not, it returns an empty string.
    :return: str - the recognized text
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите!")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language=language)
        print(f"Вы сказали: {text}")
        return text
    except sr.UnknownValueError:
        print("Извините, я не понял, что вы сказали.")
        return ''
    except sr.RequestError as e:
        print(f"Произошла ошибка {e}")
        return ''


def string_to_speech(text: str, lang: str = 'ru') -> None:
    """
    Convert a given `text` string to speech in the specified `lang` language using Google's Text-to-Speech (gTTS) API.
    If `text` is empty, raise a `ValueError`. 
    Save the speech output as an mp3 file named "response.mp3" and play it using the `playsound` library.
    
    :param text: The string to be converted to speech.
    :type text: str
    :param lang: The language in which the speech output should be generated. Default is 'ru'.
    :type lang: str
    :return: None
    :rtype: None
    """
    if not text:
        raise ValueError('text is empty!')
    tts = gTTS(text=text, lang=lang)
    tts.save("response.mp3")
    playsound("response.mp3")
