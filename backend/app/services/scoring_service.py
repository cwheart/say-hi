import logging
from typing import List, Dict, Any

from Levenshtein import distance as levenshtein_distance

from app.services.text_utils import tokenize

logger = logging.getLogger(__name__)


def align_words(target_words: List[str], recognized_words: List[str]) -> List[Dict[str, Any]]:
    """
    Perform word-level alignment between target and recognized text using
    dynamic programming (edit distance alignment).

    Returns a list of alignment entries, each with:
        - target: the target word (or None if extra)
        - recognized: the recognized word (or None if missing)
        - status: 'correct', 'incorrect', 'missing', or 'extra'
    """
    n = len(target_words)
    m = len(recognized_words)

    # Build DP table
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if target_words[i - 1] == recognized_words[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # deletion (missing)
                    dp[i][j - 1],      # insertion (extra)
                    dp[i - 1][j - 1],  # substitution (incorrect)
                )

    # Backtrace to build alignment
    alignment = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and target_words[i - 1] == recognized_words[j - 1]:
            alignment.append({
                "target": target_words[i - 1],
                "recognized": recognized_words[j - 1],
                "status": "correct",
            })
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            # Substitution → incorrect
            alignment.append({
                "target": target_words[i - 1],
                "recognized": recognized_words[j - 1],
                "status": "incorrect",
            })
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            # Deletion → missing from recognized
            alignment.append({
                "target": target_words[i - 1],
                "recognized": None,
                "status": "missing",
            })
            i -= 1
        else:
            # Insertion → extra word in recognized
            alignment.append({
                "target": None,
                "recognized": recognized_words[j - 1],
                "status": "extra",
            })
            j -= 1

    alignment.reverse()
    return alignment


def calculate_scores(
    alignment: List[Dict[str, Any]],
    target_words: List[str],
    recognized_words: List[str],
    segments: List[dict] = None,
) -> Dict[str, Any]:
    """
    Calculate multi-dimension pronunciation scores.

    Dimensions:
        - accuracy: % of non-extra alignment entries that are correct
        - completeness: % of target words that were spoken (correct or incorrect)
        - fluency: estimated from segment confidence (if available), default 70

    Returns:
        Dict with accuracy, completeness, fluency, overall scores (0-100).
    """
    if not target_words:
        return {
            "accuracy": 0,
            "completeness": 0,
            "fluency": 0,
            "overall": 0,
        }

    correct_count = sum(1 for a in alignment if a["status"] == "correct")
    incorrect_count = sum(1 for a in alignment if a["status"] == "incorrect")
    missing_count = sum(1 for a in alignment if a["status"] == "missing")

    total_target = len(target_words)

    # Accuracy: correct / (correct + incorrect + missing)
    evaluated = correct_count + incorrect_count + missing_count
    accuracy = round((correct_count / evaluated * 100) if evaluated > 0 else 0)

    # Completeness: (correct + incorrect) / total_target
    spoken = correct_count + incorrect_count
    completeness = round((spoken / total_target * 100) if total_target > 0 else 0)

    # Fluency: based on Whisper segment confidence if available
    fluency = _estimate_fluency(segments)

    # Overall: weighted average
    overall = round(accuracy * 0.5 + completeness * 0.3 + fluency * 0.2)

    # Clamp all values to 0-100
    return {
        "accuracy": min(max(accuracy, 0), 100),
        "completeness": min(max(completeness, 0), 100),
        "fluency": min(max(fluency, 0), 100),
        "overall": min(max(overall, 0), 100),
    }


def _estimate_fluency(segments: List[dict] = None) -> int:
    """
    Estimate fluency score from Whisper segments.

    Uses average no_speech_prob (lower is better) and avg_logprob (higher is better)
    as proxies for fluency.

    Returns a score 0-100.
    """
    if not segments:
        return 70  # Default when no segment info

    avg_logprobs = []
    no_speech_probs = []

    for seg in segments:
        if "avg_logprob" in seg:
            avg_logprobs.append(seg["avg_logprob"])
        if "no_speech_prob" in seg:
            no_speech_probs.append(seg["no_speech_prob"])

    if not avg_logprobs:
        return 70

    # avg_logprob typically ranges from -1.0 (poor) to 0.0 (perfect)
    mean_logprob = sum(avg_logprobs) / len(avg_logprobs)
    # Map to 0-100 scale: -1.0 -> 0, -0.1 -> 100
    logprob_score = max(0, min(100, (mean_logprob + 1.0) / 0.9 * 100))

    # no_speech_prob: 0 = definitely speech, 1 = definitely not speech
    if no_speech_probs:
        mean_no_speech = sum(no_speech_probs) / len(no_speech_probs)
        speech_score = (1.0 - mean_no_speech) * 100
    else:
        speech_score = 80

    # Combine: weight logprob more heavily
    fluency = round(logprob_score * 0.7 + speech_score * 0.3)
    return min(max(fluency, 0), 100)


def evaluate_pronunciation(
    target_text: str,
    recognized_text: str,
    segments: List[dict] = None,
) -> Dict[str, Any]:
    """
    Full pronunciation evaluation pipeline.

    Args:
        target_text: The reference text the user should have spoken.
        recognized_text: The text transcribed by Whisper.
        segments: Whisper segment data for fluency estimation.

    Returns:
        Dict with scores and word-level alignment.
    """
    target_words = tokenize(target_text)
    recognized_words = tokenize(recognized_text)

    alignment = align_words(target_words, recognized_words)
    scores = calculate_scores(alignment, target_words, recognized_words, segments)

    return {
        "target_text": target_text,
        "recognized_text": recognized_text,
        "scores": scores,
        "word_comparison": alignment,
    }
