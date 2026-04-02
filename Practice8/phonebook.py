import psycopg2
from connect import get_connection

def add_or_update(name, phone):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Calling the Upsert Procedure
            cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
            conn.commit()

def search(pattern):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Calling the Search Function
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
            for row in cur.fetchall():
                print(row)

def bulk_insert(names_list, phones_list):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Calling the Bulk Insert Procedure
            cur.execute("CALL bulk_insert_contacts(%s, %s)", (names_list, phones_list))
            conn.commit()

def show_page(limit, offset):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Calling the Pagination Function
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            for row in cur.fetchall():
                print(row)

def remove(identifier):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Calling the Delete Procedure
            cur.execute("CALL delete_contact_by_data(%s)", (identifier,))
            conn.commit()

def main():
    while True:
        print("\n=== PhoneBook Manager (Practice 8) ===")
        print("1. Search")
        print("2. Add/Update Contact")
        print("3. Bulk Insert")
        print("4. Show Page")
        print("5. Delete Contact")
        print("6. Exit")
        
        choice = input("\nSelect an option: ")

        try:
            if choice == '1':
                pattern = input("Enter name or phone part to search: ")
                print(f"Results for '{pattern}':")
                search(pattern)

            elif choice == '2':
                name = input("Enter name: ")
                phone = input("Enter phone: ")
                add_or_update(name, phone)
                print("Done!")

            elif choice == '3':
                # Input via comma separation: e.g., "Ivan, Maria" and "8777, 8701"
                names = input("Enter names (comma separated): ").replace(" ", "").split(",")
                phones = input("Enter phones (comma separated): ").replace(" ", "").split(",")
                if len(names) == len(phones):
                    bulk_insert(names, phones)
                    print("Bulk insert executed.")
                else:
                    print("Error: Name count must match phone count!")

            elif choice == '4':
                limit = int(input("How many records per page? "))
                offset = int(input("How many records to skip (offset)? "))
                print(f"Showing page (limit {limit}, offset {offset}):")
                show_page(limit, offset)

            elif choice == '5':
                val = input("Enter name or phone to delete: ")
                remove(val)
                print(f"Delete command sent for: {val}")

            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid choice, try again.")
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()