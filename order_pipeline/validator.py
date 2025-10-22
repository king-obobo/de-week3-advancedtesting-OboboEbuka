# Checks required fields (order_id, timestamp, item, quantity, price, payment_status, total).
# Ensures quantity, price, and total are present and positive.
# Skips rows with missing or invalid fields.

class Validator:
    
    def __init__(self, json_file: list[dict]):
        self.json_file = json_file
        self.skipped_rows: list[dict] = []
        
        # Let us define our expected keys or columns
        self.required_string_keys: list = ["order_id", "timestamp", "item", "payment_status"]
        self.required_numerical_keys: list = ["quantity", "price", "total"]
        self.expected_keys: list = self.required_string_keys + self.required_numerical_keys
        
    def validate_row(self, row:dict) -> dict | None:
        
        #We need all keys with string value to be present, if not presnt then skip row
        if any(row.get(k) in (None, "") for k in self.required_string_keys if k in row):
            self.skipped_rows.append({
                "row": row,
                "Reason": "Missing or empty required text field (s)"
            })
            return None
    
        
        # We need at least two numeric Vals to be present, we can calculate the third from there
        present_numeric_fields = {
            k: row.get(k)
            for k in self.required_numerical_keys
            if k in row and row.get(k) not in (None, "", "N/A")
        }
        
        if len(present_numeric_fields) < 2:
            self.skipped_rows.append({
                "row": row,
                "Reason": "Insufficient numeric data"
            })
            return None
        
        return row

    
    def validate_file(self):
        validated_data = []
        for idx, row in enumerate(self.json_file, start = 1):
            valid_row = self.validate_row(row)
            if valid_row:
                valid_row["_row_index"] = idx
                validated_data.append(valid_row)
        return validated_data