#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas"]
# ///
"""
Single CSV Validator for PostToolUse Hook

Validates a single CSV file after Edit|Write operations.
Reads the file path from the PostToolUse hook input JSON.

For any .csv file:
- Validates CSV can be parsed
- Validates not empty

For normalized_*.csv files (additional checks):
- Validates required columns exist
- Validates balance consistency (prev_balance - withdrawal + deposit = current_balance)

Outputs JSON decision for Claude Code hook:
- {"decision": "block", "reason": "..."} to block and retry
- {} to allow completion
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

LOG_FILE = Path(__file__).parent / "csv_single_validator.log"
PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())


def log(message: str):
    """Append timestamped message to log file."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    fd = os.open(LOG_FILE, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(fd, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def parse_numeric(val) -> float:
    """Parse a numeric value, handling empty/NaN as 0."""
    if pd.isna(val) or val == "":
        return 0.0
    return float(str(val).replace(",", "").replace("$", ""))


def is_normalized_csv(file_path: Path) -> bool:
    """Check if file is a normalized CSV that requires full validation."""
    name = file_path.name.lower()
    return name.startswith("normalized_")


def validate_csv_parseable(file_path: Path) -> list[str]:
    """Validate that a CSV file can be parsed and is not empty."""
    errors = []

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return [f"Failed to parse CSV {file_path.name}: {e}"]

    if len(df) == 0:
        errors.append(f"{file_path.name}: CSV file is empty")

    if len(df.columns) == 0:
        errors.append(f"{file_path.name}: CSV has no columns")

    return errors


def validate_normalized_csv(file_path: Path) -> list[str]:
    """Validate a normalized CSV file with column and balance checks."""
    errors = []

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return [f"Failed to parse CSV {file_path.name}: {e}"]

    required_columns = [
        "date",
        "description",
        "category",
        "deposit",
        "withdrawal",
        "balance",
        "account_name",
    ]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        errors.append(f"{file_path.name}: Missing required columns: {missing}")
        return errors

    if len(df) < 2:
        return errors

    try:
        deposits = [parse_numeric(v) for v in df["deposit"]]
        withdrawals = [parse_numeric(v) for v in df["withdrawal"]]
        balances = [parse_numeric(v) for v in df["balance"]]
        dates = list(df["date"])
    except Exception as e:
        errors.append(f"{file_path.name}: Error parsing numeric values: {e}")
        return errors

    error_count = 0
    max_errors = 3

    for i in range(len(df) - 2, -1, -1):
        prev_idx = i + 1
        curr_idx = i

        prev_balance = balances[prev_idx]
        curr_deposit = deposits[curr_idx]
        curr_withdrawal = withdrawals[curr_idx]
        curr_balance = balances[curr_idx]

        expected_balance = prev_balance - curr_withdrawal + curr_deposit

        if abs(expected_balance - curr_balance) > 0.01:
            error_count += 1
            if error_count <= max_errors:
                errors.append(
                    f"{file_path.name} row {curr_idx + 2} (date: {dates[curr_idx]}): "
                    f"Balance mismatch! Expected ${expected_balance:,.2f}, got ${curr_balance:,.2f}"
                )

    if error_count > max_errors:
        errors.append(f"... and {error_count - max_errors} more balance errors")

    return errors


def main():
    log("=" * 50)
    log("CSV SINGLE VALIDATOR (PostToolUse)")
    log(f"sys.argv: {sys.argv}")

    file_path = None
    try:
        stdin_data = sys.stdin.read()
        log(f"stdin_data length: {len(stdin_data)}")
        if stdin_data.strip():
            hook_input = json.loads(stdin_data)
            log(f"hook_event: {hook_input.get('hook_event_name')}")
            log(f"tool_name: {hook_input.get('tool_name')}")

            tool_input = hook_input.get("tool_input", {})
            file_path = tool_input.get("file_path")
            log(f"file_path: {file_path}")
    except json.JSONDecodeError as e:
        log(f"JSON decode error: {e}")
    except Exception as e:
        log(f"Error reading stdin: {e}")

    if not file_path and len(sys.argv) > 1:
        file_path = sys.argv[1]
        log(f"file_path (from arg): {file_path}")

    if not file_path:
        log("No file path provided, skipping validation")
        print(json.dumps({}))
        return

    file_path = Path(file_path)

    if file_path.suffix.lower() != ".csv":
        log(f"Skipping non-CSV file: {file_path.name}")
        print(json.dumps({}))
        return

    if not file_path.exists():
        log(f"File not found: {file_path}")
        print(json.dumps({}))
        return

    resolved = file_path.resolve()
    if not str(resolved).startswith(str(Path(PROJECT_DIR).resolve()) + "/"):
        log(f"Skipping file outside project: {resolved}")
        print(json.dumps({}))
        return

    log(f"Validating: {file_path.name}")
    errors = []

    parse_errors = validate_csv_parseable(file_path)
    errors.extend(parse_errors)

    if is_normalized_csv(file_path) and not parse_errors:
        log("  Running normalized CSV validation (columns + balance)")
        normalized_errors = validate_normalized_csv(file_path)
        errors.extend(normalized_errors)

    if errors:
        log(f"RESULT: BLOCK ({len(errors)} errors)")
        for err in errors:
            log(f"  - {err}")
        print(
            json.dumps(
                {
                    "decision": "block",
                    "reason": f"Resolve this CSV error in {file_path.name}:\n"
                    + "\n".join(errors),
                }
            )
        )
    else:
        log(f"RESULT: PASS - {file_path.name} validated")
        print(json.dumps({}))


if __name__ == "__main__":
    main()
