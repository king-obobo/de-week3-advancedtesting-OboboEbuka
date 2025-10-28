import json
from pathlib import Path
# import logging
from .logging_config import setup_logger

# Setting up the logger
reader_logger = setup_logger(__name__)


class ReadJson:
    """
    A simple class to handle reading the reading of the json file
    """
    def __init__(self, file_path:str) -> None:
        self.file_path = file_path


    # Opens the json file and returns the json
    def _open_json_file(self) -> json:
        """
        A helper function to load the json file

        Returns:
            json: _description_
        """
        with open(self.file_path, "r") as f:
            return json.load(f)


    def _validate_path_and_size(self) -> None: 
        """
        A helper method to validate that the file is a json file (ends with '.json')

        Raises:
            ValueError: To state that the file is not a json file

        Returns:
            None
        """
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
        """
        A method to tie the helper functions together

        Raises:
            ValueError: Is raised when the file is empty or if the format is invalid or if an unexpected error occurs
            

        Returns:
            list[dict]: Returns the validate data as a list of dictionaries
        """

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
        
