from utils.file_handler import read_sales_file
from utils.data_processor import clean_and_validate_data
from utils.api_handler import fetch_product_info

def main():
    file_path = "data/sales_data.txt"

    lines = read_sales_file(file_path)
    valid_records = clean_and_validate_data(lines)

    print("\nSample API Response:")
    product_info = fetch_product_info()
    print(product_info)

if __name__ == "__main__":
    main()
