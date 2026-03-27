from datetime import datetime


def now_time_string() -> str:
    return datetime.now().strftime("%I:%M %p")
