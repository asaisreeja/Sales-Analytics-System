# def clean_and_validate_data(lines):
#     total_records = 0
#     invalid_records = 0
#     valid_records = []

#     for line in lines:
#         line = line.strip()

#         # Skip empty lines
#         if not line:
#             continue

#         total_records += 1
#         fields = line.split('|')

#         # Must have exactly 8 fields
#         if len(fields) != 8:
#             invalid_records += 1
#             continue

#         transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = fields

#         # Validation rules
#         if not transaction_id.startswith('T'):
#             invalid_records += 1
#             continue

#         if customer_id == "" or region == "":
#             invalid_records += 1
#             continue

#         try:
#             quantity = int(quantity.replace(',', ''))
#             unit_price = float(unit_price.replace(',', ''))
#         except ValueError:
#             invalid_records += 1
#             continue

#         if quantity <= 0 or unit_price <= 0:
#             invalid_records += 1
#             continue

#         # Clean product name
#         product_name = product_name.replace(',', '')

#         valid_records.append({
#             "transaction_id": transaction_id,
#             "date": date,
#             "product_id": product_id,
#             "product_name": product_name,
#             "quantity": quantity,
#             "unit_price": unit_price,
#             "customer_id": customer_id,
#             "region": region
#         })

#     print(f"Total records parsed: {total_records}")
#     print(f"Invalid records removed: {invalid_records}")
#     print(f"Valid records after cleaning: {len(valid_records)}")

#     return valid_records

"""
utils/data_processor.py
Handles Part 2: Data Processing (Sales analysis, trends, and product performance).
"""
import os
from datetime import datetime

def calculate_total_revenue(transactions):
    """Calculates total revenue (Sum of Quantity * UnitPrice)."""
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)

def region_wise_sales(transactions):
    """Analyzes sales by region and sorts by total_sales descending."""
    regions = {}
    total_rev = calculate_total_revenue(transactions)
    
    for t in transactions:
        reg = t['Region']
        rev = t['Quantity'] * t['UnitPrice']
        if reg not in regions:
            regions[reg] = {'total_sales': 0.0, 'transaction_count': 0}
        regions[reg]['total_sales'] += rev
        regions[reg]['transaction_count'] += 1
    
    for reg in regions:
        regions[reg]['percentage'] = round((regions[reg]['total_sales'] / total_rev) * 100, 2)
    
    return dict(sorted(regions.items(), key=lambda x: x[1]['total_sales'], reverse=True))

def top_selling_products(transactions, n=5):
    """Finds top n products by total quantity sold."""
    products = {}
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        rev = qty * t['UnitPrice']
        if name not in products:
            products[name] = {'qty': 0, 'rev': 0.0}
        products[name]['qty'] += qty
        products[name]['rev'] += rev
        
    product_list = [(name, data['qty'], data['rev']) for name, data in products.items()]
    product_list.sort(key=lambda x: x[1], reverse=True)
    return product_list[:n]

def customer_analysis(transactions):
    """Analyzes customer spending and unique products bought."""
    customers = {}
    for t in transactions:
        c_id = t['CustomerID']
        rev = t['Quantity'] * t['UnitPrice']
        p_name = t['ProductName']
        
        if c_id not in customers:
            customers[c_id] = {'total_spent': 0.0, 'purchase_count': 0, 'products': set()}
        
        customers[c_id]['total_spent'] += rev
        customers[c_id]['purchase_count'] += 1
        customers[c_id]['products'].add(p_name)
        
    result = {}
    for c_id, data in customers.items():
        result[c_id] = {
            'total_spent': round(data['total_spent'], 2),
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(data['total_spent'] / data['purchase_count'], 2),
            'products_bought': sorted(list(data['products']))
        }
    return dict(sorted(result.items(), key=lambda x: x[1]['total_spent'], reverse=True))

def daily_sales_trend(transactions):
    """Groups revenue and customer counts by date."""
    trends = {}
    for t in transactions:
        date = t['Date']
        rev = t['Quantity'] * t['UnitPrice']
        cust = t['CustomerID']
        if date not in trends:
            trends[date] = {'revenue': 0.0, 'transaction_count': 0, 'customers': set()}
        trends[date]['revenue'] += rev
        trends[date]['transaction_count'] += 1
        trends[date]['customers'].add(cust)
        
    result = {}
    for date in sorted(trends.keys()):
        result[date] = {
            'revenue': round(trends[date]['revenue'], 2),
            'transaction_count': trends[date]['transaction_count'],
            'unique_customers': len(trends[date]['customers'])
        }
    return result

def find_peak_sales_day(transactions):
    """Returns (date, revenue, count) for the highest revenue day."""
    trend = daily_sales_trend(transactions)
    if not trend: return None
    peak_date = max(trend, key=lambda d: trend[d]['revenue'])
    return (peak_date, trend[peak_date]['revenue'], trend[peak_date]['transaction_count'])

def low_performing_products(transactions, threshold=10):
    """Finds products with total quantity < threshold."""
    products = {}
    for t in transactions:
        name = t['ProductName']
        if name not in products: products[name] = {'qty': 0, 'rev': 0.0}
        products[name]['qty'] += t['Quantity']
        products[name]['rev'] += (t['Quantity'] * t['UnitPrice'])
        
    low_perf = [(name, data['qty'], data['rev']) for name, data in products.items() if data['qty'] < threshold]
    return sorted(low_perf, key=lambda x: x[1])

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report and saves it to the output folder.
    """
    # 1. Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 2. Prepare Data using functions already in this file
    total_revenue = calculate_total_revenue(transactions)
    total_count = len(transactions)
    avg_order_value = total_revenue / total_count if total_count > 0 else 0
    
    dates = [t['Date'] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"
    
    reg_stats = region_wise_sales(transactions)
    top_prods = top_selling_products(transactions, n=5)
    cust_stats = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_prods = low_performing_products(transactions, threshold=10)

    # API Enrichment Stats
    enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
    success_rate = (enriched_count / total_count * 100) if total_count > 0 else 0
    failed_products = list(set(t['ProductID'] for t in enriched_transactions if not t.get('API_Match')))

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # HEADER
            f.write("============================================\n")
            f.write(f"{'SALES ANALYTICS REPORT':^44}\n")
            f.write(f"{'Generated: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^44}\n")
            f.write(f"{'Records Processed: ' + str(total_count):^44}\n")
            f.write("============================================\n\n")

            # OVERALL SUMMARY
            f.write("OVERALL SUMMARY\n")
            f.write("-" * 44 + "\n")
            f.write(f"Total Revenue:         ${total_revenue:,.2f}\n")
            f.write(f"Total Transactions:    {total_count}\n")
            f.write(f"Average Order Value:   ${avg_order_value:,.2f}\n")
            f.write(f"Date Range:            {date_range}\n\n")

            # REGION-WISE PERFORMANCE
            f.write("REGION-WISE PERFORMANCE\n")
            f.write("-" * 44 + "\n")
            f.write(f"{'Region':<12} {'Sales':<15} {'% Total':<8} {'Count'}\n")
            for reg, stats in reg_stats.items():
                f.write(f"{reg:<12} ${stats['total_sales']:<14,.2f} {stats['percentage']:<7}% {stats['transaction_count']}\n")
            f.write("\n")

            # TOP 5 PRODUCTS
            f.write("TOP 5 PRODUCTS\n")
            f.write("-" * 44 + "\n")
            f.write(f"{'Rank':<5} {'Product Name':<18} {'Qty':<5} {'Revenue'}\n")
            for i, (name, qty, rev) in enumerate(top_prods, 1):
                f.write(f"{i:<5} {name:<18} {qty:<5} ${rev:,.2f}\n")
            f.write("\n")

            # TOP 5 CUSTOMERS
            f.write("TOP 5 CUSTOMERS\n")
            f.write("-" * 44 + "\n")
            f.write(f"{'Rank':<5} {'Customer ID':<12} {'Total Spent':<15} {'Orders'}\n")
            top_customers = list(cust_stats.items())[:5]
            for i, (cid, data) in enumerate(top_customers, 1):
                f.write(f"{i:<5} {cid:<12} ${data['total_spent']:<14,.2f} {data['purchase_count']}\n")
            f.write("\n")

            # DAILY SALES TREND
            f.write("DAILY SALES TREND\n")
            f.write("-" * 44 + "\n")
            f.write(f"{'Date':<12} {'Revenue':<15} {'Sales':<6} {'Cust'}\n")
            for date, data in daily_trend.items():
                f.write(f"{date:<12} ${data['revenue']:<14,.2f} {data['transaction_count']:<6} {data['unique_customers']}\n")
            f.write("\n")

            # PRODUCT PERFORMANCE ANALYSIS
            f.write("PRODUCT PERFORMANCE ANALYSIS\n")
            f.write("-" * 44 + "\n")
            f.write(f"Best Selling Day: {peak_day[0]} (${peak_day[1]:,.2f})\n")
            f.write(f"Low Performing Products: {len(low_prods)} items\n\n")

            # API ENRICHMENT SUMMARY
            f.write("API ENRICHMENT SUMMARY\n")
            f.write("-" * 44 + "\n")
            f.write(f"Products Enriched: {enriched_count}\n")
            f.write(f"Success Rate:      {success_rate:.2f}%\n")
            if failed_products:
                f.write(f"Failed IDs:        {', '.join(failed_products[:3])}...\n")

        print(f"\nComprehensive report generated successfully: {output_file}")
    except Exception as e:
        print(f"Error generating report: {e}")