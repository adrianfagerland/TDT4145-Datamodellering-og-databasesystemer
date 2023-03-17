
import database
import interface

def main():
    conn = database.create_connection("togdb.sqlite")
    database.setup_database(conn)

    interface.init(conn)
        

if __name__ == "__main__":
    main()
