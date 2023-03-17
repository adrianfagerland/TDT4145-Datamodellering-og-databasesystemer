
import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn

def execute_sql_file(conn, sql_file_path):
    with open(sql_file_path, 'r') as file:
        sql_commands = file.read().split(';')
        for command in sql_commands:
            if command.strip():
                conn.execute(command)

def setup_database(conn):
    with open("lag_tabeller.sql", "r") as file:
        create_tables_script = file.read()
    try:
        cursor = conn.cursor()
        cursor.executescript(create_tables_script)
        conn.commit()
    except sqlite3.Error as e:
        print("Error executing SQL script:", e)
    
    # execute_sql_file(conn, "insert_nordlandsbanen.sql")
    execute_sql_file(conn, "insert_togruter.sql")
    # execute_sql_file(conn, "insert_billetter.sql")
    

