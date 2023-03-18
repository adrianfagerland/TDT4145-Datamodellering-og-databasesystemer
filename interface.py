import user_stories

def get_user_input():
    action = input("Ditt valg: ")
    return action

def show_menu():
    print("\nVelg et alternativ:")
    print("1: Hent togruter for en stasjon på en gitt ukedag")
    print("2: Søk etter togruter mellom to stasjoner")
    print("3: Registrer en ny kunde")
    print("4: Finn ledige billetter og kjøp")
    print("5: Vis informasjon om fremtidige reiser for en kunde")
    print("0: Avslutt programmet")

def input_station() -> str:
    return input("Stasjon: ")

def input_ukedag() -> str:
    i = input("Ukedag: ").lower()
    if i not in ("mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"):
        print("Ugyldig ukedag")
        return input_ukedag()
    return i
        
def init(conn):
    while True:
        show_menu()
        i = get_user_input()
        if i == "0":
            break
        if i < "0" or i > "5":
            print("Ugyldig valg")
            continue
        user_stories.handle(conn, i)