"""Basic input checks; incident relevance is checked separately by the AI."""

import re
import unicodedata

MAX_DESCRIPTION_LENGTH = 5000
DETAIL_MESSAGE = (
    "Please describe what happened in a short sentence, for example: "
    "'A senior threatened me outside the hostel.' Names and evidence are optional."
)


def validate_description(description: str) -> str:
    description = unicodedata.normalize("NFC", description).strip()
    if len(description) > MAX_DESCRIPTION_LENGTH:
        raise ValueError("Please keep your description within 5,000 characters.")

    letters = [char.casefold() for char in description if char.isalpha()]
    if len(letters) < 5 or len(set(letters)) < 3:
        raise ValueError(DETAIL_MESSAGE)

    # Latin-script text needs at least two words. Other scripts may express an
    # incident in one word, so defer their word boundaries to semantic analysis.
    non_latin_script = any(char.isalpha() and ord(char) > 0x024F for char in description)
    words = re.findall(r"[^\W\d_]+", description, flags=re.UNICODE)
    if not non_latin_script and len(words) < 2:
        raise ValueError(DETAIL_MESSAGE)
    if len(words) >= 4 and len({word.casefold() for word in words}) == 1:
        raise ValueError(DETAIL_MESSAGE)

    return description
