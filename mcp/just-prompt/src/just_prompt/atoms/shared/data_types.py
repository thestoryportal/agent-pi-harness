"""Shared data types for just-prompt."""

from enum import Enum
from typing import Optional


class ModelProviders(Enum):
    """LLM provider enum with short/long name aliases."""

    OPENAI = ("openai", ["o", "openai"])
    ANTHROPIC = ("anthropic", ["a", "anthropic"])
    GEMINI = ("gemini", ["g", "gemini"])
    GROQ = ("groq", ["q", "groq"])
    DEEPSEEK = ("deepseek", ["d", "deepseek"])
    OLLAMA = ("ollama", ["l", "ollama"])

    def __init__(self, full_name: str, aliases: list[str]):
        self.full_name = full_name
        self.aliases = aliases

    @classmethod
    def from_name(cls, name: str) -> Optional["ModelProviders"]:
        """Resolve a short or full provider name to a ModelProviders enum member."""
        for provider in cls:
            if name in provider.aliases:
                return provider
        return None

    @classmethod
    def all_names(cls) -> list[str]:
        """Return all full provider names."""
        return [p.full_name for p in cls]
