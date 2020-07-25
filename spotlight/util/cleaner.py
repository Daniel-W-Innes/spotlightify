import re

NAME_RE = re.compile(r"[^a-z0-9\s]+")


def name(s: str) -> str:
    return NAME_RE.sub('', s.lower())
