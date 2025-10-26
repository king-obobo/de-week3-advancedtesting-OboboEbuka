import json
import pytest
from pathlib import Path
from order_pipeline.reader import ReadJson


# Create a temporary json file to test code with
@pytest.fixture
def temp_json_file(tmp_path: Path):
    file_path = tmp_path / "test.json"
    yield file_path


# Let us test for other format other than a json file
@pytest.mark.parametrize("wrong_file_format", 
                        ["test_file.csv", "test_file.xslx", "test_file.txt"]
                        )
def test_not_json_file(wrong_file_format):
    reader = ReadJson(wrong_file_format)
    with pytest.raises(ValueError, match = "File is not a JSON file"):
        reader.read_json_file()


# Test for a non existent json file
def test_missing_file():
    reader = ReadJson("non-existent-json.json")
    with pytest.raises(FileNotFoundError, match = "File not Found"):
        reader.read_json_file()
        

# Test for an empty json file
def test_empty_json_file(temp_json_file):
    temp_json_file.write_text("")
    reader = ReadJson(str(temp_json_file))
    with pytest.raises(ValueError, match = "File is Empty"):
        reader.read_json_file()

        
# Test for bad json Data
def test_bad_json_data(temp_json_file):
    temp_json_file.write_text("{Bad Json File}")
    reader = ReadJson(str(temp_json_file))
    with pytest.raises(ValueError, match= "Invalid JSON format"):
        reader.read_json_file()
        

# Testing for a valid json file
def test_valid_json(temp_json_file):
    data = [
        {
        "order_id": "ORD001",
        "timestamp": "2025-10-19T08:00:00Z",
        "item": "Wireless Mouse",
        "quantity": 2,
        "price": "$15.99",
        "total": "$31.98",
        "payment_status": "paid"}
    ]
    
    temp_json_file.write_text(json.dumps(data))
    
    reader = ReadJson(str(temp_json_file))
    result = reader.read_json_file()
    
    # Checks it returns a list of dictionaries
    assert isinstance(result, list)
    # checks the first Item
    assert result[0]["order_id"] == "ORD001"