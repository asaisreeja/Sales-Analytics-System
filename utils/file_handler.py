# utils/file_handler.py

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw transaction lines (strings)
    """

    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

                cleaned_lines = []

                # Skip header row and empty lines
                for line in lines[1:]:
                    line = line.strip()
                    if line:
                        cleaned_lines.append(line)

                return cleaned_lines

        except UnicodeDecodeError:
            # Try next encoding
            continue

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file with supported encodings.")
    return []


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """

    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        try:
            transaction = {
                'TransactionID': parts[0].strip(),
                'Date': parts[1].strip(),
                'ProductID': parts[2].strip(),

                # Remove commas from product name
                'ProductName': parts[3].replace(',', '').strip(),

                # Convert Quantity to int
                'Quantity': int(parts[4].replace(',', '').strip()),

                # Convert UnitPrice to float
                'UnitPrice': float(parts[5].replace(',', '').strip()),

                'CustomerID': parts[6].strip(),
                'Region': parts[7].strip()
            }

            transactions.append(transaction)

        except ValueError:
            # Skip rows where conversion fails
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """

    valid_transactions = []
    invalid_count = 0

    available_regions = set()
    transaction_amounts = []

    # Collect regions and amounts for display
    for t in transactions:
        if t.get('Region'):
            available_regions.add(t['Region'])
            transaction_amounts.append(t['Quantity'] * t['UnitPrice'])

    if transaction_amounts:
        print("Available Regions:", available_regions)
        print(
            "Transaction Amount Range:",
            min(transaction_amounts),
            "-",
            max(transaction_amounts)
        )

    filtered_by_region = 0
    filtered_by_amount = 0

    for t in transactions:

        # Validation rules
        if (
            t['Quantity'] <= 0 or
            t['UnitPrice'] <= 0 or
            not t['TransactionID'].startswith('T') or
            not t['ProductID'].startswith('P') or
            not t['CustomerID'].startswith('C') or
            not t['Region']
        ):
            invalid_count += 1
            continue

        amount = t['Quantity'] * t['UnitPrice']

        # Region filter
        if region and t['Region'] != region:
            filtered_by_region += 1
            continue

        # Minimum amount filter
        if min_amount and amount < min_amount:
            filtered_by_amount += 1
            continue

        # Maximum amount filter
        if max_amount and amount > max_amount:
            filtered_by_amount += 1
            continue

        valid_transactions.append(t)

    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(valid_transactions)
    }

    return valid_transactions, invalid_count, summary
