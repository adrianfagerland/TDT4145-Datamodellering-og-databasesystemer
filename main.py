
import database
import interface

def main():
    cursor = database.init()
    interface.init(cursor)
        

if __name__ == "__main__":
    main()
