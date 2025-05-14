import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Connect to SQLite DB (or create it)
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    note TEXT,
    date TEXT
)
''')
conn.commit()

def add_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category (Food, Travel, Shopping, etc.): ")
    note = input("Enter a short note (optional): ")
    date = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute("INSERT INTO expenses (amount, category, note, date) VALUES (?, ?, ?, ?)", 
                   (amount, category, note, date))
    conn.commit()
    print("Expense added successfully.\n")

def view_expenses():
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    print("\n--- Expense Records ---")
    for row in rows:
        print(f"ID: {row[0]}, Amount: ₹{row[1]}, Category: {row[2]}, Note: {row[3]}, Date: {row[4]}")
    print()

def show_summary():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()

    if not data:
        print("No expenses to show.\n")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    print("\n--- Expense Summary ---")
    for cat, amt in zip(categories, amounts):
        print(f"{cat}: ₹{amt:.2f}")

    # Pie Chart
    plt.figure(figsize=(6,6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.title("Expense Distribution by Category")
    plt.axis('equal')
    plt.show()

def delete_expense():
    view_expenses()
    try:
        exp_id = int(input("Enter the ID of the expense to delete: "))
        cursor.execute("DELETE FROM expenses WHERE id = ?", (exp_id,))
        conn.commit()
        print("Expense deleted.\n")
    except:
        print("Invalid input.\n")

def main():
    while True:
        print("\n--- Expense Tracker Menu ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Summary (with Chart)")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Enter choice (1-5): ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            show_summary()
        elif choice == '4':
            delete_expense()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()