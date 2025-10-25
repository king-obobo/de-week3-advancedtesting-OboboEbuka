import pytest
from order_pipeline.validator import Validator


@pytest.fixture
def valid_row():
    return {
        "order_id": "ORD001",
        "timestamp": "2025-10-25T10:00:00",
        "item": "Widget",
        "payment_status": "paid",
        "quantity": 2,
        "price": 150,
        "total": 300
    }


def test_valid_row_is_accepted(valid_row):
    validator = Validator([valid_row])
    result = validator.validate_file()
    assert result == [valid_row]
    assert validator.skipped_rows == []


@pytest.mark.parametrize("bad_value", [None, "", "N/A", "N/a", "n/a"])
def test_row_with_missing_or_invalid_values_is_skipped(valid_row, bad_value):
    invalid_row = valid_row.copy()
    invalid_row["item"] = bad_value

    validator = Validator([invalid_row])
    result = validator.validate_file()

    assert result == []  
    assert len(validator.skipped_rows) == 1
    assert "Missing or empty required text field" in validator.skipped_rows[0]["Reason"]


def test_mixed_valid_and_invalid_rows(valid_row):
    invalid_row = valid_row.copy()
    
    #Insert a bad value
    invalid_row["price"] = ""

    data = [valid_row, invalid_row]
    validator = Validator(data)
    result = validator.validate_file()

    assert len(result) == 1  
    assert result[0]["order_id"] == "ORD001"
    assert len(validator.skipped_rows) == 1


def test_extra_keys_are_ignored(valid_row):
    extended_row = valid_row.copy()
    extended_row["extra_field"] = "Not needed"

    validator = Validator([extended_row])
    result = validator.validate_file()

    # Extra key should not cause any issue
    assert len(result) == 1
    assert result[0]["extra_field"] == "Not needed"


def test_empty_json_file_returns_empty_list():
    validator = Validator([])
    result = validator.validate_file()

    assert result == []
    assert validator.skipped_rows == []
