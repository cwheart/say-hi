import re
import string
from typing import List


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison:
    - Convert to lowercase
    - Remove punctuation
    - Trim and collapse whitespace

    Args:
        text: Raw input text.

    Returns:
        Normalized text string.
    """
    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Collapse whitespace and trim
    text = re.sub(r"\s+", " ", text).strip()

    return text


def tokenize(text: str) -> List[str]:
    """
    Tokenize normalized text into words.

    Args:
        text: Normalized text string.

    Returns:
        List of word tokens.
    """
    normalized = normalize_text(text)
    if not normalized:
        return []
    return normalized.split()
