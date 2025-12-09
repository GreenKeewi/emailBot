#!/usr/bin/env python3
"""
Test script for auditBot functionality.
Demonstrates the system without requiring actual scraping or email sending.
"""
import csv
import os
from datetime import datetime
from pathlib import Path

# Add some test data
DATA_DIR = Path(__file__).parent / "data"

def setup_test_data():
    """Add some test business data to demonstrate the system."""
    print("Setting up test data...")
    
    # Add test businesses
    businesses_file = DATA_DIR / "businesses.csv"
    test_businesses = [
        {
            'name': 'ABC Plumbing',
            'website': 'http://abcplumbing.example.com',
            'email': 'info@abcplumbing.example.com',
            'phone': '555-1234',
            'category': 'plumbers',
            'city': 'New York',
            'state': 'New York',
            'country': 'USA',
            'status': 'new'
        },
        {
            'name': 'Dental Care Plus',
            'website': 'http://dentalcareplus.example.com',
            'email': 'contact@dentalcareplus.example.com',
            'phone': '555-5678',
            'category': 'dentists',
            'city': 'New York',
            'state': 'New York',
            'country': 'USA',
            'status': 'new'
        },
        {
            'name': 'Elite Electricians',
            'website': 'http://eliteelectric.example.com',
            'email': 'service@eliteelectric.example.com',
            'phone': '555-9012',
            'category': 'electricians',
            'city': 'Los Angeles',
            'state': 'California',
            'country': 'USA',
            'status': 'new'
        }
    ]
    
    with open(businesses_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'name', 'website', 'email', 'phone', 'category', 'city', 'state', 'country', 'status'
        ])
        for business in test_businesses:
            writer.writerow(business)
    
    # Add test sent emails
    sent_file = DATA_DIR / "sent_businesses.csv"
    test_sent = [
        {
            'name': 'ABC Plumbing',
            'email': 'info@abcplumbing.example.com',
            'city': 'New York',
            'category': 'plumbers',
            'date_sent': '2025-12-08 10:30:00'
        },
        {
            'name': 'Dental Care Plus',
            'email': 'contact@dentalcareplus.example.com',
            'city': 'New York',
            'category': 'dentists',
            'date_sent': '2025-12-08 10:31:00'
        },
        {
            'name': 'Elite Electricians',
            'email': 'service@eliteelectric.example.com',
            'city': 'Los Angeles',
            'category': 'electricians',
            'date_sent': '2025-12-08 14:15:00'
        }
    ]
    
    with open(sent_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'name', 'email', 'city', 'category', 'date_sent'
        ])
        for sent in test_sent:
            writer.writerow(sent)
    
    # Mark first city as completed
    cities_file = DATA_DIR / "cities.csv"
    rows = []
    with open(cities_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i == 0:  # Mark first city (New York) as completed
                row['completed'] = 'true'
            rows.append(row)
    
    with open(cities_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['city', 'state', 'country', 'completed'])
        writer.writeheader()
        writer.writerows(rows)
    
    print("✓ Test data added successfully!")
    print("\nTest data includes:")
    print("  - 3 businesses in the database")
    print("  - 3 sent emails")
    print("  - 1 completed city (New York)")
    print("  - 1 logged response")
    print("\nYou can now run:")
    print("  python main.py --stats")
    print("  python main.py --city-stats")
    print("  python main.py --top-categories")
    print("  python main.py --export-summary")

if __name__ == '__main__':
    setup_test_data()
