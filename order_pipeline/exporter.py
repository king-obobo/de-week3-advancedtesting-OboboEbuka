# Writes results to shoplink_cleaned.json.
import json
import os
import logging

# Get my logger
exporter_logger = logging.getLogger(__name__)
exporter_logger.setLevel(logging.INFO)

# Setting up my handlers
exporter_file_handler = logging.FileHandler('logFiles\exporter_files.logs', mode="w")
exporter_stream_handler = logging.StreamHandler()
exporter_logger.propagate = False

# Setting levels for the handlers
exporter_file_handler.setLevel(logging.WARNING)
exporter_stream_handler.setLevel(logging.INFO)

# Setting Format for my logger
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
exporter_file_handler.setFormatter(formatter)
exporter_stream_handler.setFormatter(formatter)

# Adding my handlers to my logger
exporter_logger.addHandler(exporter_file_handler)
exporter_logger.addHandler(exporter_stream_handler)


class Exporter:
    def __init__(self, file: list, output_path:str = "JSON Files\cleaned_shoplink.json") -> str:
        self.file = file
        self.output_path = output_path
        
    # Helper function to cleanupafter corrupted file is dumped
    def _cleanup(self):
        # Delete Incomplete or corrupted output file
        try:
            if os.path.exists(self.output_path):
                os.remove(self.output_path)
                exporter_logger.info("Removed incomplete file:")
                # print(f"Removed incomplete file: {self.output_path}")
        except Exception:
            exporter_logger.exception("Clean Up Failed")
        
        
    def export_to_json(self):
        try:
            with open(self.output_path, "w") as file:
                json.dump(self.file, file, indent = 4)
            exporter_logger.info("File 'cleaned_shoplink.json' exported !!!!!")
            # print("File 'cleaned_shoplink.json' exported !!!!!")
        except TypeError as e:
            # print(f"Serialization error: {e}")
            self._cleanup()
            exporter_logger.warning("Serialization error")
            