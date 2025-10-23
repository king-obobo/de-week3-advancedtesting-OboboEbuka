# Checks required fields (order_id, timestamp, item, quantity, price, payment_status, total).
# Ensures quantity, price, and total are present and positive.
# Skips rows with missing or invalid fields.

class Validator:
    
    def __init__(self, json_file: list[dict]):
        self.json_file = json_file
        self.skipped_rows: list[dict] = []
        
        # Let us define our expected keys or columns
        self.expected_keys: list = ["order_id", "timestamp", "item", "payment_status", "quantity", "price", "total"]

        
    def _validate_row(self, row:dict) -> dict | None:
        
        #I would be dropping the row if any of the values are missing
        if any(row.get(k) in (None, "", "N/A") for k in self.expected_keys if k in row):
            self.skipped_rows.append({
                "row": row,
                "Reason": "Missing or empty required text field (s)"
            })
            return None
        
        return row

    
    def validate_file(self):
        validated_data = []
        for row in self.json_file:
            valid_row = self._validate_row(row)
            if valid_row:
                validated_data.append(valid_row)
        return validated_data