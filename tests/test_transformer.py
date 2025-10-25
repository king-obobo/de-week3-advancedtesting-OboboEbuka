import pytest
from order_pipeline.transformer import Transformer 


@pytest.fixture
def sample_data():
    return [
        {
            "order_id": "  AB123 ",
            "timestamp": "2025-10-25 10:00",
            "item": "  Apple Juice  ",
            "payment_status": "PAID ",
            "quantity": "2",
            "price": "₦4,500",
            "total": "₦9,000"
        },
        {
            "order_id": " cd456 ",
            "timestamp": "2025-10-25 11:00",
            "item": "  Banana Shake",
            "payment_status": "Pending",
            "quantity": 3,
            "price": "3.5",
            "total": 0
        }
    ]


# Let us test the helper methods
def test_extract_digits_with_numeric_values():
    t = Transformer([])
    assert t._extract_digits(45) == 45.0
    assert t._extract_digits(-12.5) == 12.5
    assert t._extract_digits(0) == 0.0


def test_extract_digits_with_string_values():
    t = Transformer([])
    assert t._extract_digits("₦4,500") == 4500
    assert t._extract_digits("123.45") == 123.45
    assert t._extract_digits("USD 200") == 200.0
    assert t._extract_digits("none") == 0.0


def test_transform_string_fields_trims_and_lowercases():
    t = Transformer([])
    row = {"order_id": "  ABC123 ", "item": "  Juice ", "payment_status": "PENDING "}
    cleaned = t._transform_string_fields(row)
    assert cleaned["order_id"] == "abc123"
    assert cleaned["item"] == "juice"
    assert cleaned["payment_status"] == "pending"


def test_transform_numeric_fields_converts_correctly():
    t = Transformer([])
    row = {"quantity": "2", "price": "3.5", "total": "7.0"}
    numeric = t._transform_numeric_fields(row)
    assert numeric["quantity"] == 2.0
    assert numeric["price"] == 3.5
    assert numeric["total"] == 7.0


def test_recalculate_total_computes_correct_value():
    t = Transformer([])
    row = {"quantity": 2, "price": 4.5}
    recalculated = t._recalculate_total(row)
    assert recalculated["total"] == 9.0


def test_recalculate_total_handles_missing_fields():
    t = Transformer([])
    row = {"quantity": 2}
    recalculated = t._recalculate_total(row)
    assert "total" not in recalculated


# ---------- TEST MAIN METHOD ----------

def test_transform_data_pipeline(sample_data):
    t = Transformer(sample_data)
    result = t.transform_data()
    
    # Check the number of rows
    assert len(result) == 2
    
    # Check string normalization
    assert result[0]["order_id"] == "ab123"
    assert result[0]["item"] == "apple juice"
    assert result[0]["payment_status"] == "paid"
    
    # Check numeric conversion
    assert isinstance(result[0]["price"], float)
    assert isinstance(result[0]["quantity"], float)
    assert isinstance(result[0]["total"], float)
    
    # Check recalculated total consistency
    assert result[0]["total"] == round(result[0]["price"] * result[0]["quantity"], 2)
    assert result[1]["total"] == round(result[1]["price"] * result[1]["quantity"], 2)


def test_transform_data_with_missing_numeric_fields():
    data = [{"order_id": "123", "item": "milk", "payment_status": "Paid"}]
    t = Transformer(data)
    result = t.transform_data()
    row = result[0]
    
    # Missing numeric fields default to 0.0
    assert row["quantity"] == 0.0
    assert row["price"] == 0.0
    assert row["total"] == 0.0


def test_transform_data_empty_input():
    t = Transformer([])
    assert t.transform_data() == []
