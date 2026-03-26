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
        with open(file_path, mode='r') as f:
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
        conn.close()

def add_contact(fname, lname, phone):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s)", (fname, lname, phone))
            conn.commit()
            print("Contact added.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def search_contacts(pattern):
    conn = get_connection()
    with conn.cursor() as cur:
        # Searching by name or phone prefix
        cur.execute("SELECT * FROM contacts WHERE first_name ILIKE %s OR phone_number LIKE %s", (f"%{pattern}%", f"{pattern}%"))
        results = cur.fetchall()
        for row in results:
            print(row)
    conn.close()

def delete_contact(identifier):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM contacts WHERE first_name = %s OR phone_number = %s", (identifier, identifier))
        conn.commit()
        print(f"Deleted {cur.rowcount} record(s).")
    conn.close()

if __name__ == "__main__":
    create_table()
    # insert_from_csv('contacts.csv') # Uncomment after creating your CSV
    print("--- Phonebook App Loaded ---")
    # You can add a while loop here for a console menu!