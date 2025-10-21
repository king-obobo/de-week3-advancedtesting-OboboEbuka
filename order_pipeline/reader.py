import json
from pathlib import Path

# Reads Data from Json File
# Returns a list of dictionaries
# Raises Valueerror for unsupported formats or empty files


# Requires the path to the json file
class ReadJson:
    def __init__(self, file_path:str) -> None:
        self.file_path = file_path


    def open_json_file(self) -> json:
        with open(self.file_path, "r") as f:
            return json.load(f)
    
    def validate_path_and_size(self) -> None: 
        # Check if file is a json file
        if not self.file_path.endswith(".json"):
            raise ValueError("File is not a JSON file")
        
        new_file_path = Path(self.file_path)
        # Check if the path exists
        if not new_file_path.exists():
            raise FileNotFoundError("File not Found")
        
        # Check if the size of the file is greater than 0
        if new_file_path.stat().st_size == 0:
            raise ValueError("File is Empty")
        
        return True
    
        
    def read_json_file(self) -> list[dict]:

        self.validate_path_and_size()
        try:
            data = self.open_json_file()
                
            if not data:
                raise ValueError("File is Empty")
            
            return data
        
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        except Exception:
            raise ValueError("Unexpected error reading File")
        

# print(Path.cwd())
reader = ReadJson("./shoplink.json")
print(reader.read_json_file())