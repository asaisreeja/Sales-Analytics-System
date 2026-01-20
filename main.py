# # main.py

# from utils.file_handler import (
#     read_sales_data,
#     parse_transactions,
#     validate_and_filter
# )

# def main():
#     print("Reading sales data file...\n")

#     raw_lines = read_sales_data("data/sales_data.txt")
#     print("Total raw records read:", len(raw_lines))

#     print("\nParsing and cleaning data...\n")
#     parsed_transactions = parse_transactions(raw_lines)
#     print("Total parsed records:", len(parsed_transactions))

#     print("\nValidating and filtering transactions...\n")
#     valid_transactions, invalid_count, summary = validate_and_filter(
#         parsed_transactions,
#         region=None,          # Example: "North"
#         min_amount=None,      # Example: 5000
#         max_amount=None       # Example: 100000
#     )

#     print("\nValidation Summary:")
#     for key, value in summary.items():
#         print(f"{key}: {value}")

#     print("\nSample Valid Transaction:")
#     if valid_transactions:
#         print(valid_transactions[0])


# if __name__ == "__main__":
#     main()
# main.py

from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

# --- NEW: Import Question 3 functions ---
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    find_peak_sales_day,
    generate_sales_report
)
from utils.api_handler import (
    fetch_all_products, 
    create_product_mapping, 
    enrich_sales_data, 
    save_enriched_data
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
        region=None,
        min_amount=None,
        max_amount=None
    )

    print("\nValidation Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")

    # --- NEW: Question 3 Reporting Section ---
    if valid_transactions:
        print("\n" + "="*30)
        print(" SALES ANALYTICS REPORT ")
        print("="*30)

        # 1. Total Revenue
        total_rev = calculate_total_revenue(valid_transactions)
        print(f"Total Revenue: ${total_rev:,.2f}")

        # 2. Regional Breakdown
        print("\nRegion-wise Sales Analysis:")
        regions = region_wise_sales(valid_transactions)
        for reg, stats in regions.items():
            print(f"- {reg}: {stats['percentage']}% (${stats['total_sales']:,.2f})")

        # 3. Top Selling Products
        print("\nTop 5 Selling Products:")
        top_5 = top_selling_products(valid_transactions, n=5)
        for name, qty, rev in top_5:
            print(f"- {name}: {qty} units sold (${rev:,.2f})")

        # 4. Peak Sale Day
        peak_day = find_peak_sales_day(valid_transactions)
        print(f"\nPeak Sales Day: {peak_day[0]} (${peak_day[1]:,.2f})")

        # 5. Top Customer
        print("\nTop Spender Details:")
        all_customers = customer_analysis(valid_transactions)
        top_id = list(all_customers.keys())[0]
        top_data = all_customers[top_id]
        print(f"- Customer ID: {top_id}")
        print(f"- Total Spent: ${top_data['total_spent']:,.2f}")
        print(f"- Products: {', '.join(top_data['products_bought'])}")
    else:
        print("\nNo valid transactions found for analysis.")

    # 1. Fetch from API
    api_products = fetch_all_products()
    
    if api_products:
        # 2. Create lookup mapping
        mapping = create_product_mapping(api_products)
        
        # 3. Enrich the sales data
        enriched_data = enrich_sales_data(valid_transactions, mapping)
        
        # 4. Save to file
        save_enriched_data(enriched_data)
        
        # Sample print to verify
        print("\nSample Enriched Row:")
        print(enriched_data[0])
    else:
        print("Skipping enrichment because API data could not be fetched.")
        
    print("\nFinalizing system and generating report...")
    generate_sales_report(valid_transactions, enriched_data)
if __name__ == "__main__":
    main()