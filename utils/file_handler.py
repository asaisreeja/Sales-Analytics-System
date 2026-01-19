def read_sales_file(file_path):
    """
    Reads sales data file and returns all lines.
    Handles non-UTF8 encoding.
    """
    with open(file_path, 'r', encoding='latin-1') as file:
        lines = file.readlines()
    return lines
