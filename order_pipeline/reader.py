import json
from pathlib import Path
import logging

# Reads Data from Json File
# Returns a list of dictionaries
# Raises Valueerror for unsupported formats or empty files


reader_logger = logging.getLogger(__name__)
reader_logger.setLevel(logging.INFO)

# Setting up my handlers
reader_file_handler = logging.FileHandler('logFiles\my_reader_files.logs', mode = "w")
reader_stream_handler = logging.StreamHandler()
reader_logger.propagate = False

# Setting levels for the handlers
reader_file_handler.setLevel(logging.WARNING)

# Setting up a formatter for my logger
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
reader_file_handler.setFormatter(formatter)
reader_stream_handler.setFormatter(formatter)

# Adding my handlerrs to my logger
reader_logger.addHandler(reader_file_handler)
reader_logger.addHandler(reader_stream_handler)

# Requires the path to the json file
class ReadJson:
    def __init__(self, file_path:str) -> None:
        self.file_path = file_path


    # Opens the json file and returns the json
    def _open_json_file(self) -> json:
        with open(self.file_path, "r") as f:
            return json.load(f)


    def _validate_path_and_size(self) -> None: 
        # Check if file is a json file
        if not self.file_path.endswith(".json"):
            reader_logger.error("File is not a JSON File")
            raise ValueError("File is not a JSON file")
        
        new_file_path = Path(self.file_path)
        # Check if the path exists
        if not new_file_path.exists():
            reader_logger.error("File not Found")
            raise FileNotFoundError("File not Found")
        
        # Check if the size of the file is greater than 0
        if new_file_path.stat().st_size == 0:
            reader_logger.error("File is Empty")
            raise ValueError("File is Empty")
        
        return True
    
        
    def read_json_file(self) -> list[dict]:

        self._validate_path_and_size()
        try:
            data = self._open_json_file()
                
            if not data:
                reader_logger.exception("File is Empty")
                raise ValueError("File is Empty")
            
            return data
        
        except json.JSONDecodeError:
            reader_logger.exception("Invalid JSON format")
            raise ValueError("Invalid JSON format")
        
        except Exception:
            reader_logger.exception("Unexpected error reading File")
            raise ValueError("Unexpected error reading File")
        
