"""
utils/api_handler.py
Handles fetching external product data from DummyJSON API and enriching local sales data.
"""
import requests

def fetch_all_products():
    """Fetches all products from DummyJSON API using limit=100."""
    url = "https://dummyjson.com/products?limit=100"
    try:
        print("Connecting to DummyJSON API...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("Successfully fetched products from API.")
            data = response.json()
            return data.get('products', [])
        else:
            print(f"API Error: Received status code {response.status_code}")
            return []
    except Exception as e:
        print(f"Connection Failed: {e}")
        return []

def create_product_mapping(api_products):
    """Creates a dictionary mapping numeric IDs to product info for fast lookup."""
    mapping = {}
    for product in api_products:
        p_id = product.get('id')
        mapping[p_id] = {
            'title': product.get('title'),
            'category': product.get('category'),
            'brand': product.get('brand'),
            'rating': product.get('rating')
        }
    return mapping

def enrich_sales_data(transactions, product_mapping):
    """Enriches transaction data with API info using numeric ProductID matching."""
    enriched_list = []
    
    for t in transactions:
        # 1. Extract numeric ID from ProductID (e.g., 'P101' -> 101)
        # We remove the 'P' and convert the rest to an integer
        try:
            raw_id = t['ProductID']
            numeric_id = int(raw_id.replace('P', ''))
        except (ValueError, AttributeError):
            numeric_id = -1
        
        # 2. Check if this numeric_id exists in our API mapping
        if numeric_id in product_mapping:
            info = product_mapping[numeric_id]
            t['API_Category'] = info['category']
            t['API_Brand'] = info['brand']
            t['API_Rating'] = info['rating']
            t['API_Match'] = True
        else:
            t['API_Category'] = None
            t['API_Brand'] = None
            t['API_Rating'] = None
            t['API_Match'] = False
            
        enriched_list.append(t)
        
    return enriched_list

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """Saves enriched transactions to a pipe-delimited file."""
    if not enriched_transactions:
        print("No enriched data to save.")
        return

    # Define headers
    headers = [
        'TransactionID', 'Date', 'ProductID', 'ProductName', 'Quantity', 
        'UnitPrice', 'CustomerID', 'Region', 'API_Category', 'API_Brand', 
        'API_Rating', 'API_Match'
    ]

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write header
            f.write("|".join(headers) + "\n")
            
            # Write data rows
            for t in enriched_transactions:
                row = [str(t.get(h, '')) for h in headers]
                f.write("|".join(row) + "\n")
        print(f"Enriched data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving enriched data: {e}")