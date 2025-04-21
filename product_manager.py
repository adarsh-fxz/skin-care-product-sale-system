"""
Product Manager Module

This module handles all product-related operations including loading, saving,
and managing product data in the WeCare Skin Care Product System.
"""

def load_products(filename):
    """
    Load products from the given filename.

    Args:
        filename (str): The name of the file to load products from

    Returns:
        list: A list of dictionaries containing product data
    """
    products = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    id_val, name, brand, stock, cost_price, origin = line.strip().split(', ')
                    products.append({
                        'id': int(id_val),
                        'name': name,
                        'brand': brand,
                        'stock': int(stock),
                        'cost_price': float(cost_price),
                        'origin': origin
                    })
    except FileNotFoundError:
        # Create file with sample data if it doesn't exist
        sample_data = [
            "1, Vitamin C Serum, Garnier, 200, 1000, France",
            "2, Skin Cleanser, Cetaphil, 100, 280, Switzerland",
            "3, Sunscreen, Aqualogica, 200, 700, India"
        ]
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('\n'.join(sample_data))
        return load_products(filename)
    return products

def save_products(products, filename):
    """
    Save products to the given filename.

    Args:
        products (list): List of product dictionaries to save
        filename (str): The name of the file to save products to
    """
    with open(filename, 'w', encoding='utf-8') as file:
        for product in products:
            line = (f"{product['id']}, {product['name']}, {product['brand']}, "
                   f"{product['stock']}, {product['cost_price']}, {product['origin']}\n")
            file.write(line)

def get_next_id(products):
    """Get the next available product ID."""
    max_id = 0
    for product in products:
        if product['id'] > max_id:
            max_id = product['id']
    return max_id + 1

def create_product_manager(filename):
    """Create a product manager with the given filename."""
    # Load the products from file
    all_products = load_products(filename)

    # Create the manager functions
    def get_products():
        return all_products

    def update_product_stock(product_id, new_stock):
        for product in all_products:
            if product['id'] == product_id:
                product['stock'] = new_stock
                save_products(all_products, filename)
                break

    def handle_restock(restock_items):
        for item in restock_items:
            product_found = False
            # Update existing product
            for product in all_products:
                if product['id'] == item['id']:
                    product['stock'] += item['quantity']
                    product['cost_price'] = item['cost_price']
                    product['brand'] = item['brand']
                    product['origin'] = item['origin']
                    product_found = True
                    break

            # Add new product
            if not product_found:
                new_id = get_next_id(all_products)
                all_products.append({
                    'id': new_id,
                    'name': item['name'],
                    'brand': item['brand'],
                    'stock': item['quantity'],
                    'cost_price': item['cost_price'],
                    'origin': item['origin']
                })
        save_products(all_products, filename)

    # Return the manager functions
    return {
        'products': all_products,
        'get_all_products': get_products,
        'update_stock': update_product_stock,
        'restock_products': handle_restock
    }
