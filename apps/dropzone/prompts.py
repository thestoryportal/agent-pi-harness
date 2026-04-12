"""Reusable prompt template engine with FILE_PATH injection."""

import re
from pathlib import Path

# Reject filenames containing prompt-injection patterns (instruction overrides,
# shell metacharacters in sequence, or embedded newlines).
_UNSAFE_FILENAME_RE = re.compile(
    r"[\n\r]"                       # embedded newlines
    r"|ignore\s+previous"           # common prompt injection prefix
    r"|system\s*:"                  # role injection
    r"|<\s*/?\s*(?:system|user)\b"  # XML-style role tags
)


def sanitize_file_path(file_path: str) -> str:
    """Reject file paths whose basename contains prompt-injection patterns."""
    basename = Path(file_path).name
    if _UNSAFE_FILENAME_RE.search(basename.lower()):
        raise ValueError(
            f"Filename rejected — contains unsafe pattern: {basename!r}"
        )
    return file_path


def load_prompt_template(prompt_path: str) -> str:
    """Load a prompt template file. Raises FileNotFoundError if missing."""
    path = Path(prompt_path)
    if not path.exists():
        raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
    return path.read_text()


def render_prompt(template: str, file_path: str) -> str:
    """Replace {FILE_PATH} placeholder in template with the actual file path."""
    return template.replace("{FILE_PATH}", file_path)


def load_and_render_prompt(prompt_path: str, file_path: str) -> str:
    """Load a prompt template and inject the file path."""
    template = load_prompt_template(prompt_path)
    return render_prompt(template, file_path)
