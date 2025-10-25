# Runs all steps

from reader import ReadJson
from validator import Validator
from transformer import Transformer
from analyzer import Analyzer
from exporter import Exporter
from datetime import datetime


if __name__ == "__main__":

    my_file = ReadJson("shoplink.json").read_json_file()
    validator = Validator(my_file)
    validated_file = validator.validate_file()
    transformed_data = Transformer(validated_file).transform_data()
    # print(type(validated_file))
    for row in validated_file:
        print(row)
        
    print("\nSKIPPED ROWS")
    for row in validator.skipped_rows:
        print(row)

    print("\nVALIDATED DATA")
    for row in transformed_data:
        print(row)

    my_analyzer = Analyzer(transformed_data)
    total_revenue = my_analyzer.compute_total_revenue()
    print(f"\nThe Total Revenue generated is ${total_revenue}")
    average_revenue = my_analyzer.compute_average_revenue()
    print(f"The Average Revenue generated is ${average_revenue}\n")
    
    print("\n====================SUMMARY STATISTICS FOR PAYMENT STATUS=========================")
    payment_status = my_analyzer.compute_payment_status()
    print(f"Total Paid payment status: {payment_status['paid']}")
    print(f"Total Pending payment status: {payment_status['pending']}")
    print(f"Total Refunded payment status: {payment_status['refunded']}")
    print("\n====================END OF SUMMARY STATISTICS FOR PAYMENT STATUS=========================\n")
    
    # bad_data = [
    #     {"not_ok": {1, 2, 3}},           # set
    #     {"not_ok": datetime.now()},      # datetime
    #     {"not_ok": b"bytes"}]           # bytes
    # test_data = [123]
    # Exporter(bad_data).export_to_json()

    Exporter(transformed_data).export_to_json()