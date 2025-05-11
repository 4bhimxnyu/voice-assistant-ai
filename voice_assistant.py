import os
import speech_recognition as sr
import pyttsx3
import openai  # Correct import

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen and convert speech to text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            print("Speech service is down.")
            return ""

# Function to get response from OpenAI
def get_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"Error with OpenAI API: {e}")
        return "Sorry, I couldn't process your request at the moment."

# Main loop
def main():
    speak("Hi, how can I help you today?")
    while True:
        query = listen()
        if query:
            if "exit" in query.lower():
                speak("Goodbye!")
                break
            response = get_response(query)
            print(f"Assistant: {response}")
            speak(response)

if __name__ == "__main__":
    main()
print(os.getenv("OPENAI_API_KEY"))
