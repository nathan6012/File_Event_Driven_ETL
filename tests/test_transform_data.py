import pytest
import pandas as pd

from worker.transform_data import transform_data


# =========================
# FIXTURES
# =========================

@pytest.fixture
def clean_data():
    return [
        {
            "data.Customer_Name": "John",
            "data.Age": 30,
            "data.Email": "john@test.com",
            "data.Purchase_Amount": 100,
            "data.Purchase_Quantity": 2,
            "data.Discount": "10%",
            "data.Region": "East",
            "data.Purchase_Date": "2026-01-10"
        }
    ]


@pytest.fixture
def unclean_data():
    return [
        {
            "data.Customer_Name": None,
            "data.Age": None,
            "data.Email": "",
            "data.Purchase_Amount": None,
            "data.Purchase_Quantity": None,
            "data.Discount": "5%",
            "data.Region": "West",
            "data.Purchase_Date": None
        }
    ]


# =========================
# TEST 1: OUTPUT TYPE
# =========================

def test_returns_list(clean_data, unclean_data):
    result = transform_data(clean_data, unclean_data)

    assert isinstance(result, list)
    assert len(result) >= 1


# =========================
# TEST 2: REQUIRED FIELDS EXIST
# =========================

def test_required_fields(clean_data, unclean_data):
    result = transform_data(clean_data, unclean_data)

    row = result[0]

    assert "customer_name" in row
    assert "purchase_amount" in row
    assert "purchase_quantity" in row


# =========================
# TEST 3: DEFAULT FILLING RULES
# =========================

def test_fallback_values(unclean_data):
    result = transform_data([], unclean_data)

    row = result[0]

    assert row["customer_name"] == "Must have a name "
    assert row["purchase_amount"] == 0.0
    assert row["purchase_quantity"] == 0


# =========================
# TEST 4: TYPE CASTING

def test_type_casting(clean_data, unclean_data):
    result = transform_data(clean_data, unclean_data)

    row = result[0]

    assert isinstance(row["purchase_amount"], float)
    assert isinstance(row["purchase_quantity"], int)


# =========================
# TEST 5: DISCOUNT CLEANING

def test_discount_cleaning(clean_data, unclean_data):
    result = transform_data(clean_data, unclean_data)

    row = result[0]

    assert row["discount"] == 10.0


# =========================
# TEST 6: EMAIL CLEANING

def test_email_cleanup(clean_data, unclean_data):
    result = transform_data([], unclean_data)

    row = result[0]

    assert row["email"] in ["NoEmail", "noemail"]


# =========================
# TEST 7: EMPTY INPUT SAFETY

def test_empty_input():
    result = transform_data([], [])

    assert result == []