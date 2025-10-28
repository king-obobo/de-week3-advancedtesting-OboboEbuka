# Assumption here is that I am dealing with a valid json file after reading it using my reader
import pytest
from pathlib import Path
from order_pipeline.exporter import Exporter
import json
from datetime import datetime

# Testing Normal List of Dictionaries
def test_export_to_json_success(tmp_path):
    data = [{
        "name": "Product A",
        "price": 1200
    }]
    file_path = tmp_path / "cleaned_shoplink.json"
    
    exporter = Exporter(data, output_path= file_path)
    exporter.export_to_json()
    
    # Tests that the file has been created
    assert file_path.exists()
    
    with open(file_path, "r") as f:
        content = json.load(f)
    
    #Tests the content
    assert data == content
    
    


# Testing bad Inputs
def test_export_to_json_error(tmp_path, capsys):
    bad_data = [
        {"not_ok": {1, 2, 3}},           # set
        {"not_ok": datetime.now()},      # datetime
        {"not_ok": b"bytes"}]
    
    file_path = tmp_path / "bad.json"
    
    exporter = Exporter(bad_data, output_path=file_path)
    exporter.export_to_json()
    
    assert not file_path.exists()
    

def test_cleanup_remove_file(tmp_path, capsys):
    file_path = tmp_path / "to_delete.json"
    file_path.write_text("temporary file")

    exporter = Exporter([], output_path=file_path)
    exporter._cleanup()

    assert not file_path.exists()
