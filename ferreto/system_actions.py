import os
import platform
import shutil
import subprocess
import urllib.parse
import webbrowser
from datetime import datetime

from ferreto.utils import now_time_string


YOUTUBE_URL = "https://www.youtube.com"
GOOGLE_SEARCH_URL = "https://www.google.com/search?q="


APP_ALIASES = {
    "notepad": ["notepad"],
    "calculator": ["calc", "gnome-calculator", "kcalc"],
    "paint": ["mspaint"],
    "vscode": ["code"],
    "chrome": [
        r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        "google-chrome",
        "chrome",
        "chromium",
        "chromium-browser",
    ],
}


def _is_windows() -> bool:
    return platform.system().lower().startswith("win")


def _resolve_executable(candidates: list[str]) -> str | None:
    for candidate in candidates:
        if os.path.isabs(candidate) and os.path.exists(candidate):
            return candidate
        found = shutil.which(candidate)
        if found:
            return found
    return None


def find_chrome_path() -> str | None:
    return _resolve_executable(APP_ALIASES["chrome"])


def _open_in_chrome(url: str) -> bool:
    chrome_path = find_chrome_path()
    if not chrome_path:
        return False

    try:
        subprocess.Popen([chrome_path, url])
        return True
    except Exception:
        return False


def open_youtube() -> str:
    if _open_in_chrome(YOUTUBE_URL):
        return "Opening YouTube in Chrome."

    webbrowser.open(YOUTUBE_URL)
    return "Chrome not found, opening YouTube in your default browser."


def search_in_chrome(query: str) -> str:
    if not query.strip():
        return "Tell me what to search for."

    encoded_query = urllib.parse.quote_plus(query)
    url = f"{GOOGLE_SEARCH_URL}{encoded_query}"

    if _open_in_chrome(url):
        return f"Searching Chrome for {query}."

    webbrowser.open(url)
    return f"Chrome not found, searching in your default browser for {query}."


def open_website(name_or_url: str) -> str:
    target = name_or_url.strip().lower()
    if not target:
        return "Please tell me which website to open."

    if not target.startswith("http"):
        if "." not in target:
            target = f"https://www.{target}.com"
        else:
            target = f"https://{target}"

    if _open_in_chrome(target):
        return f"Opening {target} in Chrome."

    webbrowser.open(target)
    return f"Opening {target} in your default browser."


def open_app(app_name: str) -> str:
    app_name = app_name.strip().lower()
    if not app_name:
        return "Tell me which app to open."

    aliases = APP_ALIASES.get(app_name, [app_name])
    executable = _resolve_executable(aliases)

    if not executable:
        return f"I could not find {app_name} on this computer."

    try:
        subprocess.Popen([executable])
        return f"Opening {app_name}."
    except Exception:
        return f"I found {app_name} but could not start it."


def get_time() -> str:
    return f"Current time is {now_time_string()}."


def get_date() -> str:
    return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."


def system_info() -> str:
    return f"You are running {platform.system()} {platform.release()}."


def open_file_or_folder(path: str) -> str:
    path = path.strip().strip('"')
    if not path:
        return "Please provide a file or folder path."
    if not os.path.exists(path):
        return "That path does not exist."

    try:
        if _is_windows():
            os.startfile(path)  # type: ignore[attr-defined]
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        return f"Opening {path}."
    except Exception:
        return "I couldn't open that path."
