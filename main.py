
import database
import interface

def main():
    conn = database.init()
    interface.init(conn)
    conn.close()
        

if __name__ == "__main__":
    main()
