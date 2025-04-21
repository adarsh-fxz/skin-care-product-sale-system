"""
Invoice Manager Module

This module handles all invoice-related operations including generating
sale and restock invoices in the WeCare Skin Care Product System.
"""

import os
from datetime import datetime

def make_invoice_filename(invoice_dir, prefix):
    """Create a unique invoice filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(invoice_dir, f"{prefix}_{timestamp}.txt")

def write_sale_invoice(invoice_dir, invoice_data):
    """Write a sale invoice to file."""
    filename = make_invoice_filename(invoice_dir, "sale")
    with open(filename, 'w', encoding='utf-8') as file:
        # Write header
        file.write("=== WeCare Skin Care - Sale Invoice ===\n\n")
        file.write(f"Date: {invoice_data['date'].strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Customer: {invoice_data['customer_name']}\n\n")

        # Write items header
        file.write("Items Purchased:\n")
        file.write("-" * 85 + "\n")
        file.write(
            f"{'ID':<5} {'Product':<20} {'Brand':<15} {'Qty':<8} {'Free':<8} "
            f"{'Price(Rs)':<12} {'Total(Rs)':<12}\n"
        )
        file.write("-" * 85 + "\n")

        # Write items
        for item in invoice_data['items']:
            file.write(
                f"{item['id']:<5} {item['name']:<20} {item['brand']:<15} "
                f"{item['quantity']:<8} {item['free_items']:<8} "
                f"{item['price']:<12.2f} {item['total']:<12.2f}\n"
            )

        # Write footer
        file.write("-" * 85 + "\n")
        file.write(f"Total Amount: Rs. {invoice_data['total_amount']:.2f}\n")
        file.write("\nThank you for shopping with WeCare!")

def write_restock_invoice(invoice_dir, invoice_data):
    """Write a restock invoice to file."""
    filename = make_invoice_filename(invoice_dir, "restock")
    with open(filename, 'w', encoding='utf-8') as file:
        # Write header
        file.write("=== WeCare Skin Care - Restock Invoice ===\n\n")
        file.write(f"Date: {invoice_data['date'].strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Supplier: {invoice_data['supplier_name']}\n\n")

        # Write items header
        file.write("Items Restocked:\n")
        file.write("-" * 80 + "\n")
        file.write(
            f"{'ID':<5} {'Product':<20} {'Brand':<15} {'Qty':<8} "
            f"{'Cost(Rs)':<15} {'Total(Rs)':<15}\n"
        )
        file.write("-" * 80 + "\n")

        # Write items
        for item in invoice_data['items']:
            item_total = item['quantity'] * item['cost_price']
            file.write(
                f"{item['id'] if item['id'] else 'NEW':<5} {item['name']:<20} "
                f"{item['brand']:<15} {item['quantity']:<8} "
                f"{item['cost_price']:<15.2f} {item_total:<15.2f}\n"
            )

        # Write footer
        file.write("-" * 80 + "\n")
        file.write(f"Total Cost: Rs. {invoice_data['total_amount']:.2f}\n")
        file.write("\nThank you for your business!")

def create_invoice_manager():
    """Create an invoice manager."""
    # Create invoices directory if it doesn't exist
    invoice_dir = "invoices"
    if not os.path.exists(invoice_dir):
        os.makedirs(invoice_dir)

    # Create the manager functions
    def handle_sale_invoice(invoice_data):
        write_sale_invoice(invoice_dir, invoice_data)

    def handle_restock_invoice(invoice_data):
        write_restock_invoice(invoice_dir, invoice_data)

    # Return the manager functions
    return {
        'generate_sale_invoice': handle_sale_invoice,
        'generate_restock_invoice': handle_restock_invoice
    }
