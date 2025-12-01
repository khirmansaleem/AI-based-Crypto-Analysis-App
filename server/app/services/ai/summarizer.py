import re

_summarizer = None  # compatibility


# patterns to remove repeated or irrelevant lines
_IRRELEVANT_PATTERNS = [
    r"cover art.*",
    r"illustration via.*",
    r"image includes.*",
    r"image (credit|via).*",
    r"shown in figure.*",
    r"figure [0-9]+.*",
    r"follow us on.*",
    r"advertisement.*",
    r"editorial note.*",
    r"read more.*",
    r"companydisclaimers.*",
    r"posted .* ago.*",
]


def _is_irrelevant(line: str) -> bool:
    lower = line.lower().strip()
    for pat in _IRRELEVANT_PATTERNS:
        if re.match(pat, lower):
            return True
    return False


def summarize_text_high_signal_sentences(text: str, max_sentences=4):
    """
    Extracts the first 3–4 meaningful sentences,
    ignoring garbage lines and filler.
    """

    cleaned = re.sub(r"\s+", " ", text.strip())
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)

    meaningful = []

    for s in sentences:
        s_clean = s.strip()

        # remove garbage
        if _is_irrelevant(s_clean):
            continue

        # skip tiny/noise lines
        if len(s_clean) < 20:
            continue

        meaningful.append(s_clean)

        if len(meaningful) >= max_sentences:
            break

    # fallback: first paragraph slice
    if not meaningful:
        return cleaned[:450].strip()

    return " ".join(meaningful).strip()


def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = summarize_text_high_signal_sentences
    return _summarizer


def generate_summary(text: str, max_sentences: int = 3):
    """
    Public API remains same.
    """
    if not text:
        return ""

    cleaned = text.strip().replace("\n", " ")
    summarizer = get_summarizer()

    try:
        return summarizer(cleaned, max_sentences=max_sentences)
    except Exception:
        return cleaned[:450] + "..."
