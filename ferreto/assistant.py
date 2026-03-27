import re

from ferreto.knowledge import answer_question
from ferreto.speech import SpeechEngine
from ferreto.system_actions import (
    get_date,
    get_time,
    open_app,
    open_file_or_folder,
    open_website,
    open_youtube,
    search_in_chrome,
    system_info,
)


class FerretoAssistant:
    def __init__(self, wake_phrase: str = "hey ferreto") -> None:
        self.wake_phrase = wake_phrase
        self.speech = SpeechEngine()
        self.active = True

    def _smalltalk(self, command: str) -> str | None:
        smalltalk_map = {
            "who are you": "I am Ferreto AI, your personal voice assistant.",
            "how are you": "I am running perfectly and ready to help.",
            "thank you": "You're welcome.",
        }
        for key, value in smalltalk_map.items():
            if key in command:
                return value
        return None

    def _extract_after(self, command: str, prefixes: list[str]) -> str:
        for prefix in prefixes:
            if command.startswith(prefix):
                return command[len(prefix) :].strip()
        return ""

    def _handle_command(self, command: str) -> str:
        command = command.strip().lower()

        if smalltalk := self._smalltalk(command):
            return smalltalk

        if "open youtube" in command or "play youtube" in command:
            return open_youtube()

        if command.startswith("search in chrome ") or command.startswith("search chrome "):
            query = self._extract_after(command, ["search in chrome ", "search chrome "])
            return search_in_chrome(query)

        if command.startswith("search "):
            query = self._extract_after(command, ["search "])
            return search_in_chrome(query)

        if command.startswith("open app "):
            app_name = self._extract_after(command, ["open app "])
            return open_app(app_name)

        if command.startswith("open file ") or command.startswith("open folder "):
            path = self._extract_after(command, ["open file ", "open folder "])
            return open_file_or_folder(path)

        if command.startswith("open website "):
            website = self._extract_after(command, ["open website "])
            return open_website(website)

        if command.startswith("open "):
            target = self._extract_after(command, ["open "])
            common_apps = {"chrome", "notepad", "calculator", "paint", "vscode"}
            if target in common_apps:
                return open_app(target)
            return open_website(target)

        if re.search(r"\btime\b", command):
            return get_time()

        if re.search(r"\bdate\b|\btoday\b", command):
            return get_date()

        if "system info" in command or "pc info" in command:
            return system_info()

        if command in {"exit", "quit", "stop", "shutdown ferreto"}:
            self.active = False
            return "Shutting down Ferreto. Goodbye."

        if command in {"sleep", "go to sleep", "standby"}:
            return "Going to passive mode. Say hey ferreto when you need me."

        return answer_question(command)

    def run(self) -> None:
        self.speech.speak("Ferreto AI online. Say hey ferreto to wake me.")

        while self.active:
            heard = self.speech.listen(timeout=6, phrase_time_limit=5)
            if not heard or self.wake_phrase not in heard:
                continue

            self.speech.speak("Yes, I am listening.")
            command = self.speech.listen(timeout=10, phrase_time_limit=14)

            if not command:
                self.speech.speak("I did not catch that. Please try again.")
                continue

            response = self._handle_command(command)
            self.speech.speak(response)
