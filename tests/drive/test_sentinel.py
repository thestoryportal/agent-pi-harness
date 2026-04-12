import re
from apps.drive.sentinel import generate_token, wrap_command, parse_sentinel


def test_generate_token_is_hex():
    token = generate_token()
    assert re.match(r"^[a-f0-9]{12}$", token)


def test_generate_token_unique():
    tokens = {generate_token() for _ in range(100)}
    assert len(tokens) == 100


def test_wrap_command():
    wrapped = wrap_command("ls -la", "abc123")
    assert wrapped == 'echo "__START_abc123" ; ls -la ; echo "__DONE_abc123:$?"'


def test_parse_sentinel_success():
    output = 'some output\n__DONE_abc123:0\nmore output'
    result = parse_sentinel(output, "abc123")
    assert result == 0


def test_parse_sentinel_failure():
    output = 'some output\n__DONE_abc123:1\n'
    result = parse_sentinel(output, "abc123")
    assert result == 1


def test_parse_sentinel_not_found():
    output = 'some output\nno sentinel here\n'
    result = parse_sentinel(output, "abc123")
    assert result is None
