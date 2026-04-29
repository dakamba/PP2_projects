import psycopg2  # Библиотека для работы с PostgreSQL
import csv       # Для работы с CSV (хотя в коде ниже не используется, может быть полезно)
import json      # Для сохранения данных в формате JSON
from connect import connect  # Твой собственный модуль для подключения к БД

# Функция для выполнения SQL-кода из внешнего файла (например, создание таблиц)
def run_sql_file(filename):
    conn = connect()  # Открываем соединение
    if not conn: return
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            sql = f.read()           # Читаем весь текст из файла
            cur = conn.cursor()      # Создаем "курсор" (объект для отправки команд в БД)
            cur.execute(sql)         # Выполняем SQL-код
            conn.commit()            # Сохраняем изменения в базе
            cur.close()              # Закрываем курсор
            print(f"File {filename} executed successfully.")
    except Exception as e:
        print(f"Error executing {filename}: {e}")
        conn.rollback()              # Если ошибка — отменяем все изменения (откат)
    finally:
        conn.close()                 # Всегда закрываем соединение в конце

# Функция для простого добавления нового контакта
def insert_contact_initial(name, email, birthday):
    conn = connect()
    if not conn: return
    try:
        cur = conn.cursor()
        # %s — это плейсхолдеры для защиты от SQL-инъекций. Данные передаются кортежем вторым аргументом.
        cur.execute("INSERT INTO contacts (first_name, email, birthday) VALUES (%s, %s, %s) RETURNING id", (name, email, birthday))
        conn.commit()
        print("Contact created.")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

# Функция для постраничного просмотра контактов (пагинация)
def get_paginated():
    conn = connect()
    if not conn: return
    limit = 5   # Сколько записей показывать на одной странице
    offset = 0  # С какой записи начинать (пропуск)
    while True:
        try:
            cur = conn.cursor()
            # Вызываем SQL-функцию, которая возвращает таблицу записей
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            rows = cur.fetchall()    # Получаем все найденные строки
            cur.close()
            
            print("\n--- Page (Offset: {}) ---".format(offset))
            if not rows:
                print("[No contacts found on this page]")
            else:
                for r in rows:
                    # r[0] - ID, r[1] - Имя, r[2] - Email (зависит от структуры возвращаемой таблицы)
                    print(f"ID: {r[0]} | Name: {r[1]} | Email: {r[2]}")
            
            # Меню навигации внутри пагинации
            nav = input("\nn=Next, p=Prev, q=Quit: ").strip().lower()
            if nav == 'n': 
                if rows: offset += limit  # Идем вперед
                else: print("No more data.")
            elif nav == 'p' and offset >= limit: 
                offset -= limit           # Идем назад
            elif nav == 'q': 
                break                     # Выход в главное меню
        except Exception as e:
            print(f"Error: {e}")
            break
    conn.close()

# Функция экспорта данных в JSON файл
def export_json(filename):
    conn = connect()
    if not conn: return
    try:
        cur = conn.cursor()
        # Делаем сложный запрос с JOIN, чтобы собрать данные из разных таблиц
        cur.execute("""
                SELECT c.first_name, c.email, TO_CHAR(c.birthday, 'YYYY-MM-DD'), g.name, p.phone, p.type 
                FROM contacts c 
                LEFT JOIN groups g ON c.group_id = g.id 
                LEFT JOIN phones p ON c.id = p.contact_id
        """)
        rows = cur.fetchall()
        data = {}
        # Превращаем плоский список строк БД в иерархическую структуру (словарь)
        for r in rows:
            name, email, bday, grp, phone, ptype = r
            if name not in data:
                # Создаем запись контакта, если его еще нет в словаре
                data[name] = {"email": email, "birthday": bday, "group": grp, "phones": []}
            if phone:
                # Если у контакта несколько телефонов, добавляем их в список
                data[name]["phones"].append({"phone": phone, "type": ptype})
        
        # Записываем словарь в файл с красивыми отступами
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Exported to {filename}.")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Точка входа в программу
if __name__ == '__main__':
    # Основной цикл меню
    while True:
        print("\n--- PhoneBook Menu ---")
        print("0. Add New Contact")
        print("1. Search")
        print("2. Add Phone to existing")
        print("3. Set Group")
        print("4. View Paginated")
        print("5. Export JSON")
        print("6. Exit")
        c = input("Choice: ")
        
        if c == '0':
            n = input("Name: ")
            e = input("Email: ")
            b = input("Birthday (YYYY-MM-DD): ")
            insert_contact_initial(n, e, b)
            
        elif c == '1':
            q = input("Query (name/email/phone): ")
            conn = connect()
            if conn:
                try:
                    cur = conn.cursor()
                    # Вызов функции поиска через SELECT
                    cur.execute("SELECT * FROM search_contacts_advanced(%s)", (q,))
                    results = cur.fetchall()
                    if not results:
                        print("Nothing found.")
                    for r in results: print(r)
                    cur.close()
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    conn.close()
                    
        elif c == '2':
            add_phone_name = input("Contact Name: ")
            phone = input("Phone: ")
            ptype = input("Type (home/work/mobile): ")
            conn = connect()
            if conn:
                try:
                    cur = conn.cursor()
                    # CALL используется для вызова хранимых процедур (PROCEDURE)
                    cur.execute("CALL add_phone(%s, %s, %s)", (add_phone_name, phone, ptype))
                    conn.commit()
                    print("Phone added successfully.")
                    cur.close()
                except Exception as e:
                    print(f"Error: {e}")
                    conn.rollback()
                finally:
                    conn.close()
                    
        elif c == '3':
            n = input("Contact Name: ")
            g = input("Group Name: ")
            conn = connect()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("CALL move_to_group(%s, %s)", (n, g))
                    conn.commit()
                    print("Group updated.")
                    cur.close()
                except Exception as e:
                    print(f"Error: {e}")
                    conn.rollback()
                finally:
                    conn.close()
                    
        elif c == '4':
            get_paginated()
            
        elif c == '5':
            export_json("contacts_export.json")
            
        elif c == '6':
            print("Goodbye!")
            break