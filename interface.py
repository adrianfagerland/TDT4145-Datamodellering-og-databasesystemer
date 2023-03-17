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
    input = input("Ukedag: ").lower()
    if input not in ("mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"):
        print("Ugyldig ukedag")
        return input_ukedag()
    return input
        
def init(conn):
    while True:
        show_menu()
        input = get_user_input()
        if input == "0":
            break
        if input < "0" or input > "5":
            print("Ugyldig valg")
            continue
        user_stories.handle(conn, input)