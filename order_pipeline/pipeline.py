# Runs all steps

from .reader import ReadJson
from .validator import Validator
from .transformer import Transformer
from .analyzer import Analyzer
from .exporter import Exporter
from datetime import datetime


class Pipeline:
    
    def __init__(self, json_file):
        self.json_file = json_file
        
        
    def run(self):
        # Read In the File
        READER = ReadJson(self.json_file)
        try:
            self.valid_json_file = READER.read_json_file()
            
            # Validate the File
            self.VALIDATOR = Validator(self.valid_json_file)
            self.validated_data = self.VALIDATOR.validate_file()
            
            # Transform Validated Data
            TRANSFORMER = Transformer(self.validated_data)
            self.transformed_data = TRANSFORMER.transform_data()
            
            # Run my Analysis
            self.ANALYZER = Analyzer(self.transformed_data)
            
        except Exception as e:
            print(f"There is something wrong with the Json file: {e}")
            
        # Export Data
        try:
            EXPORTER = Exporter(self.transformed_data)
            EXPORTER.export_to_json()
        except Exception as e:
            print("Something went wrong while exporting the File")
            
        print("===========PIPELINE RAN SUCCESSFULLY===============")
        
        
    def print_summary_statistics(self) -> None:
        
        # Prints the total Revenue
        print(f"\nThe Total Revenue generated is ${self.ANALYZER.compute_total_revenue()}")
        
        # Average Revenue
        print(f"The Average Revenue generated is ${self.ANALYZER.compute_average_revenue()}\n")
        
        print("\n====================SUMMARY STATISTICS FOR PAYMENT STATUS=========================")
        payment_status = self.ANALYZER.compute_payment_status()
        print(f"Total Paid payment status: {payment_status['paid']}")
        print(f"Total Pending payment status: {payment_status['pending']}")
        print(f"Total Refunded payment status: {payment_status['refunded']}")
        print("\n====================END OF SUMMARY STATISTICS FOR PAYMENT STATUS=========================\n")
        
        return None
    
    
    # To see the validated Data
    def get_validated_data(self):
        return self.validated_data
    
    
    # To see the transformed Data
    def get_transformed_data(self):
        return self.transformed_data
    
    
    # To see the skipped row
    def get_skipped_rows(self):
        return self.VALIDATOR.skipped_rows