# Runs all steps

from reader import ReadJson
from validator import Validator
from transformer import Transformer
from analyzer import Analyzer

my_file = ReadJson("shoplink.json").read_json_file()
validated_file = Validator(my_file).validate_file()
transformed_data = Transformer(validated_file).transform_data()
# print(type(validated_file))
# for row in validated_file:
#     print(row)
    
# print("\nSKIPPED ROWS")
# for row in validator.skipped_rows:
#     print(row)

# for row in transformed_data:
#     print(row)

my_analyzer = Analyzer(transformed_data)
total_revenue = my_analyzer.compute_total_revenue()
print(total_revenue)
average_revenue = my_analyzer.compute_average_revenue()
print(average_revenue)
payment_status = my_analyzer.compute_payment_status()
print(payment_status)