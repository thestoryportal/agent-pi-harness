"""CEO-and-board multi-model consensus tool."""

import html
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from just_prompt.atoms.shared.model_router import ModelRouter
from just_prompt.molecules.prompt import get_default_models
from just_prompt.molecules.prompt_from_file import _validate_path_within_root

logger = logging.getLogger(__name__)

CEO_PROMPT_TEMPLATE_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "prompts"
    / "ceo_prompt_template.xml"
)
DEFAULT_CEO_MODEL = "openai:o3"


def _wrap_board_response(model: str, response: str) -> str:
    """Wrap a board member response in an XML envelope."""
    safe_model = html.escape(model, quote=True)
    return (
        f'<board_member_response model="{safe_model}">\n'
        f"{response}\n"
        f"</board_member_response>"
    )


def ceo_and_board(
    abs_file_path: str,
    models_prefixed_by_provider: list[str] | None = None,
    abs_output_dir: str | None = None,
    ceo_model: str = DEFAULT_CEO_MODEL,
) -> str:
    """Send a prompt to board member models, then have CEO synthesize.

    Phase 1: Fan-out — all board members receive the prompt in parallel.
    Phase 2: Collection — each response wrapped in XML envelope.
    Phase 3: CEO synthesis — CEO receives original prompt + all responses.

    Args:
        abs_file_path: Absolute path to the prompt file.
        models_prefixed_by_provider: Board member model strings.
        abs_output_dir: Directory to save board responses and CEO decision.
        ceo_model: Model string for CEO (default: openai:o3).

    Returns:
        CEO decision text (markdown).
    """
    path = Path(abs_file_path)
    if not path.is_absolute():
        raise ValueError(
            f"abs_file_path must be absolute, got: {abs_file_path}"
        )
    path = _validate_path_within_root(path, "abs_file_path")
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {abs_file_path}")

    output_path = Path(abs_output_dir) if abs_output_dir else Path.cwd()
    if abs_output_dir and not output_path.is_absolute():
        raise ValueError(
            f"abs_output_dir must be absolute, got: {abs_output_dir}"
        )
    output_path = _validate_path_within_root(output_path, "abs_output_dir")

    original_prompt = path.read_text(encoding="utf-8")
    board_models = models_prefixed_by_provider or get_default_models()

    # Phase 1: Fan-out — parallel board member responses
    board_responses: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=max(1, len(board_models))) as executor:
        futures = {
            executor.submit(
                ModelRouter.route_prompt, model, original_prompt
            ): model
            for model in board_models
        }
        for future in as_completed(futures):
            model = futures[future]
            try:
                board_responses[model] = future.result()
            except Exception as e:
                logger.error("Board member %s error: %s", model, e)
                board_responses[model] = f"ERROR: {e}"

    # Phase 2: Collection — wrap in XML envelopes
    wrapped = "\n\n".join(
        _wrap_board_response(model, resp)
        for model, resp in board_responses.items()
    )

    # Save board responses to output dir
    output_path.mkdir(parents=True, exist_ok=True)
    for model, resp in board_responses.items():
        safe_name = model.replace(":", "_").replace("/", "_")
        (output_path / f"{safe_name}_response.md").write_text(
            resp, encoding="utf-8"
        )

    # Phase 3: CEO synthesis
    ceo_template = CEO_PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    ceo_prompt = (
        f"{ceo_template}\n\n"
        f"<original-question>\n{original_prompt}\n</original-question>\n\n"
        f"<board-responses>\n{wrapped}\n</board-responses>"
    )
    ceo_decision = ModelRouter.route_prompt(ceo_model, ceo_prompt)

    # Save CEO decision
    (output_path / "ceo_decision.md").write_text(
        ceo_decision, encoding="utf-8"
    )

    return ceo_decision
