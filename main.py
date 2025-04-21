"""
WeCare Skin Care Product System - Main Module

This module implements the main functionality of the WeCare Skin Care Product System,
including product display, sales, and restocking operations.
"""

from datetime import datetime
import product_manager
import invoice_manager

# Constants
MARKUP_PERCENTAGE = 200  # 200% markup

def get_valid_input(prompt, input_type=str, min_value=None, allow_zero=False):
    """
    Helper function to get and validate user input.
    
    Args:
        prompt (str): The prompt message to display
        input_type (type): The type of input expected (str, int, or float)
        min_value (float/int): Minimum allowed value for numeric inputs
        allow_zero (bool): Whether to allow zero as a valid input for numeric types
    
    Returns:
        The validated input of the specified type
    """
    while True:
        value = input(prompt).strip()

        if not value:
            print("Error: Input cannot be empty")
            continue

        if input_type in (int, float):
            try:
                value = input_type(value)
                if min_value is not None and value < min_value:
                    print(f"Error: Value must be greater than {min_value}")
                    continue
                if not allow_zero and value == 0:
                    print("Error: Value cannot be zero")
                    continue
            except ValueError:
                print(f"Error: Please enter a valid {input_type.__name__}")
                continue

        return value

def display_menu():
    """Display the main menu and return user's choice."""
    print("\n=== WeCare Skin Care Product System ===")
    print("1. Display all products")
    print("2. Make a sale")
    print("3. Restock products")
    print("4. Exit")
    return input("Enter your choice (1-4): ")

def display_products(products):
    """Display all products in a formatted table."""
    print("\nAvailable Products:")
    print(f"{'ID':<5} {'Name':<20} {'Brand':<15} {'Stock':<10} {'Price(Rs)':<15} {'Origin':<15}")
    print("-" * 80)
    for product in products:
        if product['stock'] > 0:
            selling_price = product['cost_price'] * (1 + MARKUP_PERCENTAGE/100)
            print(f"{product['id']:<5} {product['name']:<20} {product['brand']:<15} "
                  f"{product['stock']:<10} {selling_price:<15.2f} {product['origin']:<15}")

def process_sale_item(product, quantity):
    """Process a single sale item and return sale details."""
    if quantity <= 0:
        return None, "Quantity must be positive"
    if quantity > product['stock']:
        return None, f"Only {product['stock']} items available in stock"

    # Calculate free items (1 free for every 3 bought)
    free_items = quantity // 3
    total_items = quantity + free_items

    if total_items > product['stock']:
        return None, f"Not enough stock for free items. Maximum available: {product['stock']}"

    selling_price = product['cost_price'] * (1 + MARKUP_PERCENTAGE/100)
    item_total = quantity * selling_price

    return {
        'id': product['id'],
        'name': product['name'],
        'brand': product['brand'],
        'quantity': quantity,
        'free_items': free_items,
        'price': selling_price,
        'total': item_total
    }, None

def make_sale(product_mgr, invoice_mgr):
    """Process a sale transaction."""
    print("\n=== Make a Sale ===")
    customer_name = get_valid_input("Enter customer name: ")

    products = product_mgr['get_all_products']()
    display_products(products)

    sale_items = []
    total_amount = 0

    while True:
        try:
            product_id = input("\nEnter product ID (or 'done' to finish): ").strip()
            if product_id.lower() == 'done':
                break
            if not product_id:
                print("Error: Product ID cannot be empty")
                continue

            product_id = int(product_id)
            product = None
            for p in products:
                if p['id'] == product_id:
                    product = p
                    break

            if not product:
                print("Error: Product ID not found")
                continue

            quantity = get_valid_input(
                f"Enter quantity for {product['name']}: ",
                input_type=int,
                min_value=1
            )

            sale_item, error = process_sale_item(product, quantity)

            if error:
                print(f"Error: {error}")
                continue

            sale_items.append(sale_item)
            total_amount += sale_item['total']

            # Update stock
            product_mgr['update_stock'](product['id'],
                product['stock'] - (sale_item['quantity'] + sale_item['free_items']))

        except ValueError:
            print("Error: Please enter a valid number")
            continue

    if sale_items:
        # Generate sale invoice
        invoice_data = {
            'customer_name': customer_name,
            'date': datetime.now(),
            'items': sale_items,
            'total_amount': total_amount
        }
        invoice_mgr['generate_sale_invoice'](invoice_data)
        print(f"\nSale completed! Total amount: Rs. {total_amount:.2f}")
        print("Invoice has been generated.")

def restock_products(product_mgr, invoice_mgr):
    """Process a product restocking transaction."""
    print("\n=== Restock Products ===")
    supplier_name = get_valid_input("Enter supplier name: ")

    products = product_mgr['get_all_products']()
    display_products(products)

    restock_items = []
    total_cost = 0

    while True:
        try:
            product_id = input(
                "\nEnter product ID (or 'new' for new product, 'done' to finish): ").strip()
            if product_id.lower() == 'done':
                break
            if not product_id:
                print("Error: Product ID cannot be empty")
                continue

            if product_id.lower() == 'new':
                name = get_valid_input("Enter new product name: ")
                brand = get_valid_input("Enter brand name: ")
                origin = get_valid_input("Enter country of origin: ")
                quantity = get_valid_input(
                    "Enter quantity: ",
                    input_type=int,
                    min_value=1
                )
                cost_price = get_valid_input(
                    "Enter cost price per item: ",
                    input_type=float,
                    min_value=0.01
                )

                restock_items.append({
                    'id': None,  # New product, ID will be assigned by product manager
                    'name': name,
                    'brand': brand,
                    'quantity': quantity,
                    'cost_price': cost_price,
                    'origin': origin
                })
                total_cost += quantity * cost_price
                continue

            product_id = int(product_id)
            product = None
            for p in products:
                if p['id'] == product_id:
                    product = p
                    break

            if not product:
                print("Error: Product ID not found")
                continue

            quantity = get_valid_input(
                f"Enter quantity for {product['name']}: ",
                input_type=int,
                min_value=1
            )
            cost_price = get_valid_input(
                "Enter new cost price per item (or 0 to keep current): ",
                input_type=float,
                min_value=0,
                allow_zero=True
            )

            if cost_price == 0:
                cost_price = product['cost_price']

            restock_items.append({
                'id': product['id'],
                'name': product['name'],
                'brand': product['brand'],
                'quantity': quantity,
                'cost_price': cost_price,
                'origin': product['origin']
            })

            total_cost += quantity * cost_price

        except ValueError:
            print("Error: Please enter valid numbers")
            continue

    if restock_items:
        # Update product file
        product_mgr['restock_products'](restock_items)

        # Generate restock invoice
        invoice_data = {
            'supplier_name': supplier_name,
            'date': datetime.now(),
            'items': restock_items,
            'total_amount': total_cost
        }
        invoice_mgr['generate_restock_invoice'](invoice_data)
        print(f"\nRestock completed! Total cost: Rs. {total_cost:.2f}")
        print("Invoice has been generated.")

def main():
    """Main function to run the WeCare Skin Care Product System."""
    # Initialize managers
    product_mgr = product_manager.create_product_manager("products.txt")
    invoice_mgr = invoice_manager.create_invoice_manager()

    while True:
        choice = display_menu()

        if choice == '1':
            products = product_mgr['get_all_products']()
            display_products(products)
        elif choice == '2':
            make_sale(product_mgr, invoice_mgr)
        elif choice == '3':
            restock_products(product_mgr, invoice_mgr)
        elif choice == '4':
            print("\nThank you for using WeCare Skin Care Product System!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
