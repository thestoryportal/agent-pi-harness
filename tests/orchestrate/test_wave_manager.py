"""Tests for apps.orchestrate.wave_manager — batched parallel dispatch."""

import pytest

from apps.orchestrate.wave_manager import chunk_items, infer_mode, plan_waves


def test_single_mode_one_wave():
    waves = plan_waves(["a", "b", "c"], "single")
    assert len(waves) == 1
    assert waves[0]["items"] == ["a"]
    assert waves[0]["total_waves"] == 1


def test_small_batch_one_wave():
    waves = plan_waves(["a", "b", "c", "d", "e"], "small_batch")
    assert len(waves) == 1
    assert len(waves[0]["items"]) == 5
    assert waves[0]["total_waves"] == 1


def test_large_batch_chunked():
    items = list(range(12))
    waves = plan_waves(items, "large_batch", batch_size=5)
    assert len(waves) == 3
    assert len(waves[0]["items"]) == 5
    assert len(waves[1]["items"]) == 5
    assert len(waves[2]["items"]) == 2


def test_infinite_no_max_all_items():
    waves = plan_waves(["a", "b", "c", "d"], "infinite")
    assert len(waves) == 4
    for w in waves:
        assert len(w["items"]) == 1
        assert w["total_waves"] is None


def test_infinite_capped_by_max_waves():
    waves = plan_waves(list(range(10)), "infinite", max_waves=3)
    assert len(waves) == 3


def test_wave_numbers_are_1_indexed():
    waves = plan_waves(list(range(10)), "large_batch", batch_size=3)
    assert waves[0]["wave_number"] == 1
    assert waves[-1]["wave_number"] == len(waves)


def test_plan_empty_items_raises():
    with pytest.raises(ValueError, match="must not be empty"):
        plan_waves([], "single")


def test_plan_unknown_mode_raises():
    with pytest.raises(ValueError, match="unknown mode"):
        plan_waves(["a"], "bogus")


def test_plan_batch_size_zero_raises():
    with pytest.raises(ValueError, match="batch_size must be >= 1"):
        plan_waves(["a"], "large_batch", batch_size=0)


def test_infer_mode_single():
    assert infer_mode(1) == "single"


def test_infer_mode_small_batch():
    assert infer_mode(3) == "small_batch"


def test_infer_mode_small_batch_boundary():
    assert infer_mode(5) == "small_batch"


def test_infer_mode_large_batch():
    assert infer_mode(10) == "large_batch"


def test_infer_mode_large_batch_boundary():
    assert infer_mode(6) == "large_batch"


def test_infer_mode_infinite():
    assert infer_mode(-1) == "infinite"


def test_infer_mode_zero_raises():
    with pytest.raises(ValueError, match="must be positive"):
        infer_mode(0)


def test_infer_mode_negative_raises():
    with pytest.raises(ValueError, match="must be positive"):
        infer_mode(-2)


def test_chunk_items_even():
    assert chunk_items([1, 2, 3, 4, 5, 6], 2) == [[1, 2], [3, 4], [5, 6]]


def test_chunk_items_remainder():
    assert chunk_items([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_single_item():
    assert chunk_items(["x"], 5) == [["x"]]


def test_large_batch_total_waves_correct():
    waves = plan_waves(list(range(7)), "large_batch", batch_size=3)
    assert all(w["total_waves"] == 3 for w in waves)


def test_single_mode_with_many_items():
    waves = plan_waves(list(range(100)), "single")
    assert len(waves) == 1
    assert len(waves[0]["items"]) == 1
