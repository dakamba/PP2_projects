import psycopg2
import csv
from connect import get_connection

def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50),
        phone_number VARCHAR(15) UNIQUE NOT NULL
    );
    """
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
        conn.close()

def insert_from_csv(file_path):
    conn = get_connection()
    if not conn: return
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # Skip header
            with conn.cursor() as cur:
                cur.executemany(
                    "INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    [row for row in reader]
                )
                conn.commit()
        print("CSV data imported successfully.")
    except Exception as e:
        print(f"CSV Error: {e}")
    finally:
        if conn:
            conn.close()

def add_contact(fname, lname, phone):
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s)", (fname, lname, phone))
            conn.commit()
            print("Contact added successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def search_contacts(pattern):
    conn = get_connection()
    if not conn: return
    with conn.cursor() as cur:
        # Searching by name or phone prefix
        cur.execute("SELECT * FROM contacts WHERE first_name ILIKE %s OR phone_number LIKE %s", (f"%{pattern}%", f"{pattern}%"))
        results = cur.fetchall()
        if not results:
            print("No results found.")
        for row in results:
            print(row)
    conn.close()

def delete_contact(identifier):
    conn = get_connection()
    if not conn: return
    with conn.cursor() as cur:
        cur.execute("DELETE FROM contacts WHERE first_name = %s OR phone_number = %s", (identifier, identifier))
        conn.commit()
        print(f"Deleted.")
    conn.close()

if __name__ == "__main__":
    create_table()
    print("--- Phonebook App Loaded ---")
    
    while True:
        print("\n--- Contact Management Menu ---")
        print("1. Add contact")
        print("2. Search contact (by name or number)")
        print("3. Delete contact")
        print("4. Import from CSV")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ")
        
        if choice == '1':
            fname = input("Enter first name: ")
            lname = input("Enter last name: ")
            phone = input("Enter phone number: ")
            add_contact(fname, lname, phone)
            
        elif choice == '2':
            pattern = input("Enter name or the beginning of a phone number: ")
            search_contacts(pattern)
            
        elif choice == '3':
            identifier = input("Enter name or number to delete: ")
            delete_contact(identifier)
            
        elif choice == '4':
            file_path = input("Enter file path (e.g., contacts.csv): ")
            insert_from_csv(file_path)
            
        elif choice == '5':
            print("Exiting application...")
            break
            
        else:
            print("Error: Please select an option between 1 and 5.")
