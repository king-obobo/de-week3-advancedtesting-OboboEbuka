# Writes results to shoplink_cleaned.json.
import json
import os
# import logging
from .logging_config import setup_logger

exporter_logger = setup_logger(__name__)


class Exporter:
    """
    An Exporter Class to handle cleaned data to a json file stored in the 'JSON Files' Folder
    """
    def __init__(self, file: list, output_path:str = "JSON Files\cleaned_shoplink.json") -> str:
        self.file = file
        self.output_path = output_path
        
    # Helper function to cleanupafter corrupted file is dumped
    def _cleanup(self) -> None:
        """
        Cleans up my Directory after a failed attempt at exporting to a JSON file
        """
        # Delete Incomplete or corrupted output file
        try:
            if os.path.exists(self.output_path):
                os.remove(self.output_path)
                exporter_logger.info("Removed incomplete file:")
                # print(f"Removed incomplete file: {self.output_path}")
        except Exception:
            exporter_logger.exception("Clean Up Failed")
        
        
    def export_to_json(self) -> None:
        """
        Performs the Exporting to JSON file action
        """
        try:
            with open(self.output_path, "w") as file:
                json.dump(self.file, file, indent = 4)
            exporter_logger.info("File 'cleaned_shoplink.json' exported !!!!!")
            # print("File 'cleaned_shoplink.json' exported !!!!!")
        except TypeError as e:
            # print(f"Serialization error: {e}")
            self._cleanup()
            exporter_logger.error(f"Serialization error {e}")
            