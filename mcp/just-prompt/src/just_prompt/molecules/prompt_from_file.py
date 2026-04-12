"""Send a prompt from a file to multiple LLM models."""

from pathlib import Path

from just_prompt.molecules.prompt import prompt as prompt_fn


def prompt_from_file(
    abs_file_path: str,
    models_prefixed_by_provider: list[str] | None = None,
) -> dict[str, str]:
    """Read prompt from a file and send to multiple LLM models.

    Args:
        abs_file_path: Absolute path to the prompt file.
        models_prefixed_by_provider: List of "provider:model[:suffix]" strings.

    Returns:
        Dict mapping model string to response text.
    """
    path = Path(abs_file_path)
    if not path.is_absolute():
        raise ValueError(f"abs_file_path must be absolute, got: {abs_file_path}")
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {abs_file_path}")

    text = path.read_text(encoding="utf-8")
    return prompt_fn(text, models_prefixed_by_provider)


def prompt_from_file_to_file(
    abs_file_path: str,
    models_prefixed_by_provider: list[str] | None = None,
    abs_output_dir: str | None = None,
) -> dict[str, str]:
    """Read prompt from a file, send to models, and save responses as markdown.

    Args:
        abs_file_path: Absolute path to the prompt file.
        models_prefixed_by_provider: List of "provider:model[:suffix]" strings.
        abs_output_dir: Directory to save response markdown files.

    Returns:
        Dict mapping model string to output file path.
    """
    results = prompt_from_file(abs_file_path, models_prefixed_by_provider)

    output_path = Path(abs_output_dir) if abs_output_dir else Path.cwd()
    if abs_output_dir and not output_path.is_absolute():
        raise ValueError(
            f"abs_output_dir must be absolute, got: {abs_output_dir}"
        )
    output_path.mkdir(parents=True, exist_ok=True)

    file_paths: dict[str, str] = {}
    for model, response in results.items():
        safe_name = model.replace(":", "_").replace("/", "_")
        out_file = output_path / f"{safe_name}_response.md"
        out_file.write_text(response, encoding="utf-8")
        file_paths[model] = str(out_file)

    return file_paths
