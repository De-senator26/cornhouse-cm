"""Simple local fallback responses for the chatbot when Gemini is unavailable.

This module provides a lightweight rule-based reply generator so the UI
can still present helpful tips when the AI backend is down or quota-limited.
"""

from typing import Optional


def get_fallback_reply(message: Optional[str]) -> str:
    if not message:
        return "I can't reach the AI backend right now, but I can still help with farming tips: ask about planting, pests, or storage."

    m = message.lower()
    if any(greet in m for greet in ("hello", "hi", "hey")):
        return "Hello! I can help with farming questions like planting, pests, and storage."
    if any(k in m for k in ("plant", "planting", "seed", "sow")):
        return "For maize, plant seeds 2-3 cm deep in well-drained soil; keep rows about 75 cm apart and thin seedlings for best growth."
    if any(k in m for k in ("pest", "disease", "insect", "bug")):
        return "Monitor your crop weekly for pests; remove affected plants, use biological controls and rotate crops when possible."
    if any(k in m for k in ("fertil", "manure", "compost")):
        return "Balance nitrogen and phosphorus; add compost before planting and consider soil testing for precise recommendations."

    return "I don't have the AI backend right now, but here's a practical tip: ask about planting times, fertilizer amounts, or pest identification."
