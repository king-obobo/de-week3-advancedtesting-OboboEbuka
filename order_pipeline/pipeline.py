# Runs all steps

from reader import ReadJson
from validator import Validator
from transformer import Transformer

my_file = ReadJson("shoplink.json").read_json_file()
validated_file = Validator(my_file).validate_file()
transformed_data = Transformer(validated_file).transform_data()
# print(type(validated_file))
# for row in validated_file:
#     print(row)
    
# print("\nSKIPPED ROWS")
# for row in validator.skipped_rows:
#     print(row)

for row in transformed_data:
    print(row)

