# Converts quantity, price, and total to numeric values.
# Normalizes payment_status (paid/pending/refunded → lowercase).
# Cleans text fields (trim spaces, fix casing).
# Recalculates total = quantity * price for consistency.

import re

class Transformer:
    # ["order_id", "timestamp", "item", "payment_status", "quantity", "price", "total"]
    REQUIRED_STRING_FIELDS = ["order_id", "item", "payment_status"]
    REQUIRED_NUMERICAL_FIELDS = ["quantity", "price", "total"]
    
    
    def __init__(self, json_file: list):
        self.json_file = json_file
        
        
    def _extract_digits(self, val: str|float|int) -> None:
        if isinstance(val, (int, float)):
            return abs(float(val))
        
        if isinstance(val, str):
            match = re.search(r'[\d.,]+', val)
            if match:
                cleaned = match.group().replace(",", "")
                try:
                    return abs(float(cleaned))
                except ValueError:
                    return 0.0
                
        return 0.0
        
        
    def _transform_string_fields(self, row):
        # Cleans text fields (trim spaces, fix casing).
        for field in Transformer.REQUIRED_STRING_FIELDS:
            if field in row and isinstance(row[field], str):
                row[field] = row[field].strip().lower()
        return row
        
    
    def _transform_numeric_fields(self, row):
        # Converts quantity, price, and total to numeric values.
        for field in Transformer.REQUIRED_NUMERICAL_FIELDS:
            if field in row:
                row[field] = self._extract_digits(row[field])
            else:
                row[field] = 0.0
        return row
    
    
    def _recalculate_total(self, row: dict):
        # Recalculates total = quantity * price for consistency.
        if "quantity" in row and "price" in row:
            row["total"] = round(row['price'] * row['quantity'], 2)
        
        return row
    
    
    def transform_data(self):
        transformed_data = []
        for row in self.json_file:
            row = self._transform_string_fields(row)
            row = self._transform_numeric_fields(row)
            row = self._recalculate_total(row)
            transformed_data.append(row)
            
        return transformed_data