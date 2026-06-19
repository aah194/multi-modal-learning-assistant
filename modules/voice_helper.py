# import speech_recognition as sr
# import pyttsx3

# recognizer = sr.Recognizer()

# engine = pyttsx3.init()

# def speech_to_text():

#     with sr.Microphone() as source:

#         recognizer.adjust_for_ambient_noise(
#             source,
#             duration=1
#         )

#         audio = recognizer.listen(
#             source
#         )

#     try:

#         text = recognizer.recognize_google(
#             audio
#         )

#         return text

#     except Exception:

#         return None


# def text_to_speech(text):

#     engine.say(text)

#     engine.runAndWait()

# def text_to_speech(text):

#     engine.say(text)
#     engine.runAndWait()


# def stop_speaking():

#     engine.stop()    