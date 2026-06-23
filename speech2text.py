import speech_recognition as sr
r = sr.Recognizer()

def speech2text():
    try:
        with sr.Microphone() as source:

            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            text = text.lower()
            print(text)
            return text

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("Could not understand audio")