# Runs all steps

from .reader import ReadJson
from .validator import Validator
from .transformer import Transformer
from .analyzer import Analyzer
from .exporter import Exporter
from datetime import datetime
import logging

pipeline_logger = logging.getLogger(__name__)
pipeline_logger.setLevel(logging.INFO)

# Setting up my handlers
pipeline_file_handler = logging.FileHandler('logFiles\pipeline_files.logs', mode="w")
pipeline_stream_handler = logging.StreamHandler()
pipeline_logger.propagate = False

# Setting levels for the handlers
pipeline_file_handler.setLevel(logging.WARNING)
# pipeline_stream_handler.setLevel(logging.INFO)

# Setting Format for my logger
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
pipeline_file_handler.setFormatter(formatter)
pipeline_stream_handler.setFormatter(formatter)

# Adding my handlers to my logger
pipeline_logger.addHandler(pipeline_file_handler)
pipeline_logger.addHandler(pipeline_stream_handler)


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
            pipeline_logger.exception(f"There is something wrong with the Json file {e}")
            
            
        # Export Data
        try:
            EXPORTER = Exporter(self.transformed_data)
            EXPORTER.export_to_json()
        except Exception as e:
            pipeline_logger.exception(f"Something went wrong while exporting the File {e}")
            # print("Something went wrong while exporting the File")
            
        pipeline_logger.info("===========PIPELINE RAN SUCCESSFULLY===============")
        
        
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
    @property
    def get_validated_data(self):
        return self.validated_data
    
    
    # To see the transformed Data
    @property
    def get_transformed_data(self):
        return self.transformed_data
    
    
    # To see the skipped row
    @property
    def get_skipped_rows(self):
        return self.VALIDATOR.skipped_rows