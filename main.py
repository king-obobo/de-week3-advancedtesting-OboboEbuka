from order_pipeline.pipeline import Pipeline


if __name__ == "__main__":
    
    pipeline = Pipeline("shoplink.json")
    pipeline.run()
    pipeline.print_summary_statistics()

    print("\n============= PRINTING VALIDATED DATA=================\n")
    validate_data = pipeline.get_validated_data()
    for row in validate_data:
        print(row)
        
    print("\n============= PRINTING TRANSFORMED DATA=================\n")
    transformed_data = pipeline.get_transformed_data()
    for row in transformed_data:
        print(row)
        
    print("\n============= SKIPPED ROWS=================\n")
    skipped_data = pipeline.get_skipped_rows()
    for row in skipped_data:
        print(row)