import pytest
from order_pipeline.analyzer import Analyzer


@pytest.fixture
def sample_data():
    return [
        {"total": 1000.50, "payment_status": "paid"},
        {"total": 2000.00, "payment_status": "pending"},
        {"total": 500.25, "payment_status": "paid"},
        {"total": 250.75, "payment_status": "refunded"},
    ]


def test_compute_revenue_vals(sample_data):
    a = Analyzer(sample_data)
    total, count = a.compute_revenue_vals()
    
    assert total == round(sum(row["total"] for row in sample_data), 2)
    assert count == len(sample_data)


def test_compute_total_revenue(sample_data):
    a = Analyzer(sample_data)
    assert a.compute_total_revenue() == round(sum(row["total"] for row in sample_data), 2)


def test_compute_average_revenue(sample_data):
    a = Analyzer(sample_data)
    # (1000.5 + 2000 + 500.25 + 250.75) / 4 = 937.875
    assert a.compute_average_revenue() == round(sum(row["total"] for row in sample_data) / len(sample_data), 2)


def test_compute_payment_status_counts(sample_data):
    a = Analyzer(sample_data)
    result = a.compute_payment_status()
    assert result == {"paid": 2, "pending": 1, "refunded": 1}


def test_invalid_payment_status_ignored():
    data = [
        {"total": 100, "payment_status": "paid"},
        {"total": 200, "payment_status": "unknown"},
        {"total": 50, "payment_status": "pending"},
    ]
    a = Analyzer(data)
    result = a.compute_payment_status()
    # unknown should not affect known categories
    assert result == {"paid": 1, "pending": 1, "refunded": 0}

