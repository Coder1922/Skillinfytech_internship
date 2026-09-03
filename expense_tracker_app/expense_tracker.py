import csv
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(SCRIPT_DIR, 'expenses.csv')

def initialize_file():
    """Creates the CSV file with headers if it does not already exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount', 'Description'])

def add_expense():
    """Prompts the user to input an expense and appends it to the CSV."""
    date = datetime.now().strftime("%Y-%m-%d")
    category = input("Enter Category (e.g., Food, Travel, Pets): ").strip().title()
    description = input("Enter Description: ").strip()
    
    try:
        amount = float(input("Enter Amount: "))
    except ValueError:
        print("\nError: Please enter a valid number for the amount.")
        return

    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])
        
    print(f"\nSuccess: Added ₹{amount} for {category} to your expenses.")

def view_expenses():
    """Reads and displays all recorded expenses."""
    if not os.path.exists(FILE_NAME):
        print("\nNo expenses recorded yet.")
        return

    print("\n--- All Expenses ---")
    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            print(f"Date: {row[0]} | Category: {row[1]} | Amount: ₹{row[2]} | Desc: {row[3]}")
    print("-" * 20)

def filter_expenses():
    """Filters expenses by a specific Date or Category."""
    if not os.path.exists(FILE_NAME):
        print("\nNo expenses recorded yet.")
        return

    print("\n--- Filter Expenses ---")
    print("1. By Date (YYYY-MM-DD)")
    print("2. By Category")
    choice = input("Choose filter type (1 or 2): ").strip()

    if choice == '1':
        search_term = input("Enter Date (e.g., 2026-09-03): ").strip()
        column_index = 0
    elif choice == '2':
        search_term = input("Enter Category: ").strip().title()
        column_index = 1
    else:
        print("Invalid choice.")
        return

    print(f"\n--- Results for '{search_term}' ---")
    found = False
    filtered_total = 0.0

    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[column_index] == search_term:
                print(f"Date: {row[0]} | Category: {row[1]} | Amount: ₹{row[2]} | Desc: {row[3]}")
                filtered_total += float(row[2])
                found = True
    
    if found:
        print("-" * 22)
        print(f"Total for '{search_term}': ₹{filtered_total:.2f}")
    else:
        print("No matching expenses found.")

def generate_report():
    """Calculates and displays total spending per category."""
    if not os.path.exists(FILE_NAME):
        print("\nNo data available to generate a report.")
        return

    category_totals = {}
    total_spent = 0.0

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            amount = float(row['Amount'])
            category = row['Category']
            
            category_totals[category] = category_totals.get(category, 0) + amount
            total_spent += amount

    print("\n--- Expense Report ---")
    for category, total in category_totals.items():
        print(f"{category}: ₹{total:.2f}")
    print(f"\nTotal Spent: ₹{total_spent:.2f}")
    print("-" * 22)

def main():
    initialize_file()
    
    while True:
        print("\n=== Expense Tracker Menu ===")
        print("1. Add an Expense")
        print("2. View All Expenses")
        print("3. Filter Expenses")
        print("4. Generate Category Report")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            filter_expenses()
        elif choice == '4':
            generate_report()
        elif choice == '5':
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 5.")

if __name__ == "__main__":
    main()