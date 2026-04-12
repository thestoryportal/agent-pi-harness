import ast
import csv
import json
import os
import re
import subprocess

import pytest

SFA_DIR = os.path.join(os.path.dirname(__file__), "..", "agents", "sfa")
DATA_DIR = os.path.join(SFA_DIR, "data")

AGENTS = [
    "sfa_bash_editor_agent.py",
    "sfa_duckdb_agent.py",
    "sfa_sqlite_agent.py",
    "sfa_polars_csv_agent.py",
    "sfa_jq_agent.py",
    "sfa_meta_prompt_agent.py",
    "sfa_codebase_context_agent.py",
    "sfa_self_correcting_sql_agent.py",
]


def read_agent(name: str) -> str:
    with open(os.path.join(SFA_DIR, name)) as f:
        return f.read()


# ---------------------------------------------------------------------------
# Group 1 — Directory + fixtures
# ---------------------------------------------------------------------------


def test_sfa_dir_exists():
    assert os.path.isdir(SFA_DIR)


def test_csv_fixture_columns():
    with open(os.path.join(DATA_DIR, "analytics.csv"), newline="") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
    expected = {"id", "name", "age", "city", "score", "is_active", "status", "created_at"}
    assert expected.issubset(set(columns))


def test_csv_fixture_row_count():
    with open(os.path.join(DATA_DIR, "analytics.csv"), newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 30


def test_json_fixture_structure():
    with open(os.path.join(DATA_DIR, "analytics.json")) as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert len(data) == 30
    expected_keys = {"id", "name", "age", "city", "score", "is_active", "status", "created_at"}
    assert expected_keys == set(data[0].keys())


# ---------------------------------------------------------------------------
# Group 2 — PEP 723 structural
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("agent", AGENTS)
def test_shebang(agent):
    path = os.path.join(SFA_DIR, agent)
    with open(path) as f:
        first_line = f.readline()
    assert first_line.startswith("#!/usr/bin/env")


@pytest.mark.parametrize("agent", AGENTS)
def test_pep723_block(agent):
    content = read_agent(agent)
    assert "# /// script" in content
    assert "dependencies" in content


@pytest.mark.parametrize("agent", AGENTS)
def test_ast_parses(agent):
    content = read_agent(agent)
    ast.parse(content)  # raises SyntaxError on failure


# ---------------------------------------------------------------------------
# Group 3 — Help flag
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("agent", AGENTS)
def test_help_exits_zero(agent):
    agent_path = os.path.join(SFA_DIR, agent)
    result = subprocess.run(
        ["uv", "run", agent_path, "--help"],
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0


# ---------------------------------------------------------------------------
# Group 4 — Model standardization
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("agent", AGENTS)
def test_uses_claude37(agent):
    content = read_agent(agent)
    assert "claude-3-7-sonnet" in content


# ---------------------------------------------------------------------------
# Group 5 — Extended thinking
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("agent", AGENTS)
def test_extended_thinking(agent):
    content = read_agent(agent)
    assert "budget_tokens" in content


# ---------------------------------------------------------------------------
# Group 6 — Agent-specific tool checks
# ---------------------------------------------------------------------------


def test_bash_editor_tools():
    content = read_agent("sfa_bash_editor_agent.py")
    for tool in ["view_file", "create_file", "str_replace", "insert_line", "execute_bash", "complete_task"]:
        assert tool in content, f"Missing tool: {tool}"


def test_duckdb_tools():
    content = read_agent("sfa_duckdb_agent.py")
    for tool in ["list_tables", "describe_table", "sample_table", "run_test_sql_query", "run_final_sql_query"]:
        assert tool in content, f"Missing tool: {tool}"


def test_duckdb_table_validation():
    content = read_agent("sfa_duckdb_agent.py")
    assert "_validate_table_name" in content


def test_sqlite_tools():
    content = read_agent("sfa_sqlite_agent.py")
    for tool in ["list_tables", "describe_table", "sample_table", "run_test_sql_query", "run_final_sql_query"]:
        assert tool in content, f"Missing tool: {tool}"


def test_sqlite_uses_stdlib():
    content = read_agent("sfa_sqlite_agent.py")
    assert "import sqlite3" in content


def test_sqlite_table_validation():
    content = read_agent("sfa_sqlite_agent.py")
    assert "_validate_table_name" in content


def test_polars_tools():
    content = read_agent("sfa_polars_csv_agent.py")
    for tool in ["list_columns", "sample_csv", "run_test_polars_code", "run_final_polars_code"]:
        assert tool in content, f"Missing tool: {tool}"


def test_jq_tools():
    content = read_agent("sfa_jq_agent.py")
    for tool in ["generate_jq_command", "execute_jq_command", "complete_task"]:
        assert tool in content, f"Missing tool: {tool}"


def test_jq_no_shell_true():
    content = read_agent("sfa_jq_agent.py")
    assert "shell=True" not in content


def test_meta_prompt_tools():
    content = read_agent("sfa_meta_prompt_agent.py")
    for tool in ["generate_prompt", "complete_task"]:
        assert tool in content, f"Missing tool: {tool}"


def test_context_tools():
    content = read_agent("sfa_codebase_context_agent.py")
    for tool in [
        "git_list_files",
        "check_file_paths_line_length",
        "determine_if_files_are_relevant",
        "add_relevant_files",
        "complete_task_output_relevant_files",
    ]:
        assert tool in content, f"Missing tool: {tool}"


def test_context_parallel():
    content = read_agent("sfa_codebase_context_agent.py")
    assert "ThreadPoolExecutor" in content


def test_context_token_tracking():
    content = read_agent("sfa_codebase_context_agent.py")
    assert "display_token_usage" in content


def test_self_correcting_tools():
    content = read_agent("sfa_self_correcting_sql_agent.py")
    for tool in ["execute_sql", "complete_task"]:
        assert tool in content, f"Missing tool: {tool}"


def test_self_correcting_log():
    content = read_agent("sfa_self_correcting_sql_agent.py")
    assert "CORRECTION_LOG" in content


def test_self_correcting_max_retries():
    content = read_agent("sfa_self_correcting_sql_agent.py")
    assert "MAX_RETRIES" in content


# ---------------------------------------------------------------------------
# Group 7 — Security checks
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("agent", AGENTS)
def test_no_hardcoded_api_key(agent):
    content = read_agent(agent)
    # Block actual Anthropic API key tokens
    assert "sk-ant-" not in content
    # Block Python-level hardcoded assignments like ANTHROPIC_API_KEY = "sk-..."
    # Excludes shell export instructions (export ANTHROPIC_API_KEY=...) and placeholder strings
    assert not re.search(r'^\s*ANTHROPIC_API_KEY\s*=\s*["\']', content, re.MULTILINE)


def test_duckdb_no_shell_true():
    content = read_agent("sfa_duckdb_agent.py")
    assert "shell=True" not in content


def test_self_correcting_no_shell_true():
    content = read_agent("sfa_self_correcting_sql_agent.py")
    assert "shell=True" not in content


def test_self_correcting_db_validation():
    content = read_agent("sfa_self_correcting_sql_agent.py")
    assert "os.path.isfile" in content
