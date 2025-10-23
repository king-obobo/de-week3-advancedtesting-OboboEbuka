# Runs all steps

from reader import ReadJson
from validator import Validator

reader = ReadJson("shoplink.json") # C:\Users\DELL\Desktop\Data-Epic\Advanced-Testing-Week3\shoplink.json #shoplink.json
my_file = reader.read_json_file()

validator = Validator(my_file)
validated_file = validator.validate_file()

for row in validated_file:
    print(row)
    
print("\nSKIPPED ROWS")
for row in validator.skipped_rows:
    print(row)

