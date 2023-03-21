
import sqlite3


def init():
    conn = create_connection("sql/tog.db")
    setup_database(conn)
    return conn


def create_connection(db_file):
    conn = None
    try:
        with sqlite3.connect(db_file) as conn:
            return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def execute_sql_file(conn: sqlite3.Connection, sql_file_path):
    with open(sql_file_path, 'r') as file:
        sql_commands = file.read().split(';')
        for command in sql_commands:
            if command.strip():
                conn.execute(command)
                conn.commit()


def setup_database(conn: sqlite3.Connection):
    with open("sql/lag_tabeller.sql", "r") as file:
        create_tables_script = file.read()
    try:
        cursor = conn.cursor()
        cursor.executescript(create_tables_script)
        conn.commit()
    except sqlite3.Error as e:
        print("Error executing SQL script:", e)

    execute_sql_file(conn, "sql/insert_vogntyper.sql")
    execute_sql_file(conn, "sql/insert_nordlandsbanen.sql")
    execute_sql_file(conn, "sql/insert_togruter.sql")
    execute_sql_file(conn, "sql/insert_togruteforekomster.sql")
