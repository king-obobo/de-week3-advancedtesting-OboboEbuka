# Writes results to shoplink_cleaned.json.
import json
import os

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
                print(f"Removed incomplete file: {self.output_path}")
        except Exception as e:
            print(f"Cleanup failed: {e}")
        
        
    def export_to_json(self):
        try:
            with open(self.output_path, "w") as file:
                json.dump(self.file, file, indent = 4)
            print("File 'cleaned_shoplink.json' exported !!!!!")
        except TypeError as e:
            print(f"Serialization error: {e}")
            self._cleanup()
            