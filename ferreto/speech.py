import speech_recognition as sr
import pyttsx3


class SpeechEngine:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 175)

    def speak(self, text: str) -> None:
        print(f"Ferreto: {text}")
        self.tts.say(text)
        self.tts.runAndWait()

    def listen(self, timeout: int = 8, phrase_time_limit: int = 8) -> str | None:
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )
            except sr.WaitTimeoutError:
                return None

        try:
            heard = self.recognizer.recognize_google(audio)
            print(f"You: {heard}")
            return heard.lower().strip()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
