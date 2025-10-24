# Converts quantity, price, and total to numeric values.
# Normalizes payment_status (paid/pending/refunded → lowercase).
# Cleans text fields (trim spaces, fix casing).
# Recalculates total = quantity * price for consistency.

import json
import re

class Transformer:
    # ["order_id", "timestamp", "item", "payment_status", "quantity", "price", "total"]
    REQUIRED_STRING_FIELDS = ["order_id", "item", "payment_status"]
    REQUIRED_NUMERICAL_FIELDS = ["quantity", "price", "total"]
    
    
    def __init__(self, json_file: list):
        self.json_file = json_file
        
        
    def extract_digits(self, val: str|float|int) -> None:
        if isinstance(val, (int, float)):
            return abs(float(val))
        
        if isinstance(val, str):
            match = re.search(r'[\d.]+', val)
            if match:
                return abs(float(match.group()))
                
        return 0.0
        
        
    def transform_string_fields(self, row):
        # Cleans text fields (trim spaces, fix casing).
        for field in Transformer.REQUIRED_STRING_FIELDS:
            if field in row and isinstance(row[field], str):
                row[field] = row[field].strip().lower()
        return row
        
    
    def transform_numeric_fields(self, row):
        # Converts quantity, price, and total to numeric values.
        for field in Transformer.REQUIRED_NUMERICAL_FIELDS:
            if field in row:
                row[field] = self.extract_digits(row[field])
        return row
    
    
    def recalculate_total(self, row: dict):
        if "quantity" in row and "price" in row:
            row["total"] = round(row['price'] * row['quantity'], 2)
        # Recalculates total = quantity * price for consistency.
        return row
    
    
    def transform_data(self):
        transformed_data = []
        for row in self.json_file:
            row = self.transform_string_fields(row)
            row = self.transform_numeric_fields(row)
            row = self.recalculate_total(row)
            transformed_data.append(row)
            
        return transformed_data