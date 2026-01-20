def clean_and_validate_data(lines):
    total_records = 0
    invalid_records = 0
    valid_records = []

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        total_records += 1
        fields = line.split('|')

        # Must have exactly 8 fields
        if len(fields) != 8:
            invalid_records += 1
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = fields

        # Validation rules
        if not transaction_id.startswith('T'):
            invalid_records += 1
            continue

        if customer_id == "" or region == "":
            invalid_records += 1
            continue

        try:
            quantity = int(quantity.replace(',', ''))
            unit_price = float(unit_price.replace(',', ''))
        except ValueError:
            invalid_records += 1
            continue

        if quantity <= 0 or unit_price <= 0:
            invalid_records += 1
            continue

        # Clean product name
        product_name = product_name.replace(',', '')

        valid_records.append({
            "transaction_id": transaction_id,
            "date": date,
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "customer_id": customer_id,
            "region": region
        })

    print(f"Total records parsed: {total_records}")
    print(f"Invalid records removed: {invalid_records}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    return valid_records