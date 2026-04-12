"""Reusable prompt template engine with FILE_PATH injection."""

import re
from pathlib import Path

# Reject paths containing prompt-injection patterns anywhere in the full path
# (directory components included, not just the basename).
_UNSAFE_PATH_RE = re.compile(
    r"[\n\r\x00-\x08\x0b\x0c\x0e-\x1f]"  # control characters
    r"|ignore\s+previous"                   # common prompt injection prefix
    r"|system\s*:"                          # role injection
    r"|<\s*/?\s*(?:system|user)\b"          # XML-style role tags
, re.IGNORECASE)


def sanitize_file_path(file_path: str) -> str:
    """Reject file paths containing prompt-injection patterns or control chars.

    Checks the FULL path (all directory components + filename), not just the
    basename, to prevent injection via crafted directory names.
    """
    if _UNSAFE_PATH_RE.search(file_path):
        raise ValueError(
            f"Path rejected — contains unsafe pattern: {file_path!r}"
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
