# main.py

from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

def main():
    print("Reading sales data file...\n")

    raw_lines = read_sales_data("data/sales_data.txt")
    print("Total raw records read:", len(raw_lines))

    print("\nParsing and cleaning data...\n")
    parsed_transactions = parse_transactions(raw_lines)
    print("Total parsed records:", len(parsed_transactions))

    print("\nValidating and filtering transactions...\n")
    valid_transactions, invalid_count, summary = validate_and_filter(
        parsed_transactions,
        region=None,          # Example: "North"
        min_amount=None,      # Example: 5000
        max_amount=None       # Example: 100000
    )

    print("\nValidation Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\nSample Valid Transaction:")
    if valid_transactions:
        print(valid_transactions[0])


if __name__ == "__main__":
    main()
