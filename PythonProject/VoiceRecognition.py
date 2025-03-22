import pygame
import speech_recognition as sr
import pygame as py
import openai
import pyttsx3

engine = pyttsx3.init()

engine.setProperty('rate', 200)  # Speed of speech (default is 200)
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0, default is 1)

openai.api_key = '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'
# Initialize recognizer
recognizer = sr.Recognizer()
py.mixer.init()
isTriggerPhrase = False
# Define trigger phrase
TRIGGER_PHRASE = "hey jarvis"


def listen_for_trigger():
    """Listen for the trigger phrase before proceeding."""
    print("Listening for trigger phrase...")

    with sr.Microphone() as source:
        while True:
            print("Say something...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            try:
                # Convert speech to text
                speech_text = recognizer.recognize_google(audio).lower()  # Convert to lower case for comparison
                print(f"Recognized: {speech_text}")

                # Check if the trigger phrase was said
                if TRIGGER_PHRASE in speech_text:
                    print(f"Trigger phrase '{TRIGGER_PHRASE}' detected!")
                    py.mixer.Sound("beep.mp3").play()
                    return True  # Continue once the trigger phrase is detected
                else:
                    print(f"Trigger phrase not detected. Keep talking.")

            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")


def listen_for_query():
    """Listen for the actual query after trigger phrase is detected."""
    print("Listening for query...")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            # Recognize the speech
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the query.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")


if __name__ == "__main__":
    while True:
        if listen_for_trigger():  # Wait until the trigger phrase is detected
            query = listen_for_query()  # Now listen for the actual query
            query = query + " in 2 sentences"
            if query:
                print(f"Processed query: {query}")
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # or "gpt-3.5-turbo"
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": query}
                    ],
                    max_tokens=100
                )

                print(response['choices'][0]['message']['content'].strip())
                engine.say(response['choices'][0]['message']['content'].strip())
                engine.runAndWait()