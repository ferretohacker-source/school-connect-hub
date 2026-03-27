from typing import Iterable

import wikipedia
from duckduckgo_search import DDGS


FALLBACK_MESSAGE = (
    "I couldn't find a confident answer right now. "
    "You can ask me to search it in Chrome."
)


def _trim_sentences(text: str, max_chars: int = 450) -> str:
    text = " ".join(text.split())
    return text if len(text) <= max_chars else text[: max_chars - 3] + "..."


def _duckduckgo_answer(query: str) -> str | None:
    with DDGS() as ddgs:
        results: Iterable[dict] = ddgs.text(query, max_results=5)
        for item in results:
            title = item.get("title", "").strip()
            body = item.get("body", "").strip()
            if body:
                return _trim_sentences(f"{title}. {body}" if title else body)
    return None


def answer_question(query: str) -> str:
    """Return an Alexa-like concise answer sourced from internet knowledge."""
    wikipedia.set_lang("en")

    try:
        summary = wikipedia.summary(query, sentences=2, auto_suggest=True, redirect=True)
        if summary:
            return _trim_sentences(summary)
    except wikipedia.DisambiguationError as e:
        if e.options:
            option = e.options[0]
            try:
                return _trim_sentences(wikipedia.summary(option, sentences=2))
            except Exception:
                pass
    except Exception:
        pass

    try:
        duck = _duckduckgo_answer(query)
        if duck:
            return duck
    except Exception:
        pass

    return FALLBACK_MESSAGE
