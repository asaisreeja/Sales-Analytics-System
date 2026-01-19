import requests

def fetch_product_info():
    """
    Fetch product info from a public API.
    """
    url = "https://fakestoreapi.com/products/1"
    response = requests.get(url)
    return response.json()
