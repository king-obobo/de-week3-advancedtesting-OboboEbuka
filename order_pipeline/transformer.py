# Converts quantity, price, and total to numeric values.
# Normalizes payment_status (paid/pending/refunded → lowercase).
# Cleans text fields (trim spaces, fix casing).
# Recalculates total = quantity * price for consistency.

import re
from .logging_config import setup_logger

# Setting up my logger
trans_logger = setup_logger(__name__)

class Transformer:
    """
    A transformer class that ensures the numeric fields [quantity, price and total] are infact numeric
    """
    # ["order_id", "timestamp", "item", "payment_status", "quantity", "price", "total"]
    REQUIRED_STRING_FIELDS = ["order_id", "item", "payment_status"]
    REQUIRED_NUMERICAL_FIELDS = ["quantity", "price", "total"]
    
    
    def __init__(self, json_file: list):
        self.json_file = json_file
        
        
    def _extract_digits(self, val: str|float|int) -> float:
        """
        Uses regex to extract the digits from a string and returns it as a float. This is specific to columns that are expected to be numeric

        Args:
            val (str | float | int): A non empty string containg some digits

        Returns:
            float: The cleaned data point
        """
        if isinstance(val, (int, float)):
            return abs(float(val))
        
        if isinstance(val, str):
            match = re.search(r'[\d.,]+', val)
            if match:
                cleaned = match.group().replace(",", "")
                try:
                    return abs(float(cleaned))
                except ValueError:
                    trans_logger.error("Data could not be converted into a float, replacing with Zero...")
                    return 0.0
                
        return 0.0
        
        
    def _transform_string_fields(self, row:dict):
        """
        Cleans us the fields that are expected to be stringd

        Args:
            row (dict): a dictionary representing the row

        Returns:
            row
        """
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