# Writes results to shoplink_cleaned.json.
import json


class Exporter:
    def __init__(self, file: list) -> str:
        self.file = file
        
        
    def export_to_json(self):
        with open("cleaned_shoplink.json", "w") as file:
            json.dump(self.file, file, indent = 4)
            
        print("File 'cleaned_shoplink.json' exported !!!!!")