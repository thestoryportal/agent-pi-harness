"""Tests for list_models molecule."""

import pytest
from unittest.mock import patch

from just_prompt.molecules.list_models import list_models


@patch("just_prompt.molecules.list_models.ModelRouter")
def test_list_models_delegates_to_router(mock_router):
    """Delegates to ModelRouter.route_list_models."""
    mock_router.route_list_models.return_value = ["m1", "m2"]

    result = list_models("openai")
    assert result == ["m1", "m2"]
    mock_router.route_list_models.assert_called_once_with("openai")


@patch("just_prompt.molecules.list_models.ModelRouter")
def test_list_models_accepts_short_alias(mock_router):
    """Short alias is passed through to router."""
    mock_router.route_list_models.return_value = ["m1"]

    list_models("o")
    mock_router.route_list_models.assert_called_once_with("o")


def test_list_models_unknown_provider_raises():
    """Unknown provider raises ValueError."""
    with pytest.raises(ValueError):
        list_models("xyz")
