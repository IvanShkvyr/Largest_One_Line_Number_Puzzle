import pytest

from src.utils import create_index


class DummyParts:
    def __init__(self, value: str):
        self.value = value
        self.head = value[:2]
        self.tail = value[-2:]
        self.match_head = set()
        self.match_tail = set()


### test create_index ###

def test_create_index_elements_are_correct():
    parts = [
        DummyParts("942517"),
        DummyParts("175676"),
    ]
    result = create_index(parts, "head")

    assert result["94"][0].value == "942517"
    assert result["17"][0].value == "175676"


def test_create_index_basic_head_element():
    parts = [
        DummyParts("942517"),
        DummyParts("175676"),
        DummyParts("498294"),
        DummyParts("178894"),
    ]
    result = create_index(parts, "head")

    assert len(result) == 3
    assert len(result["94"]) == 1
    assert len(result["17"]) == 2
    assert len(result["49"]) == 1


def test_create_index_basic_tail_element():
    parts = [
        DummyParts("942517"),
        DummyParts("175676"),
        DummyParts("498294"),
        DummyParts("178894"),
    ]
    result = create_index(parts, "tail")

    assert len(result) == 3
    assert len(result["17"]) == 1
    assert len(result["76"]) == 1
    assert len(result["94"]) == 2


def test_create_index_empty_list():
    parts = []
    result_head = create_index(parts, "head")
    result_tail = create_index(parts, "tail")

    assert result_head == {}
    assert result_tail == {}


def test_create_index_attribute_not_found():
    parts = [DummyParts("125634")]

    with pytest.raises(AttributeError):
        create_index(parts, "unknown_attribute")

