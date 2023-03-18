import interface
import sqlite3


def handle(conn: sqlite3.Connection, i):
    functions = {1: get_togruter_by_stasjon_and_day, 2: search_togruter,
                 3: register_kunde, 4: find_and_buy_billetter, 5: get_kunde_reise_info}
    
    functions[int(i)](conn)

# c) Hent togruter som er innom en gitt stasjon på en gitt ukedag
def get_togruter_by_stasjon_and_day(conn):
    stasjon = interface.input_station()
    ukedag = interface.input_ukedag()
    print(ukedag)
    query = f"""
        SELECT TogruteID, Operatør, Togoppsett
        FROM Togrute
        WHERE {ukedag} = 1
        AND TogruteID IN (
            SELECT TogruteID
            FROM Togrutetabell
            WHERE Stasjon = ?
        )
    """

    # Utfør spørringen og hent resultatene
    cursor = conn.cursor()
    cursor.execute(query, (stasjon,))

    # Skriv ut resultatene
    print(
        f"Togruter som er innom stasjonen {stasjon} på {ukedag.capitalize()}:")

    for row in cursor.fetchall():
        print(f"TogruteID: {row[0]}, Operatør: {row[1]}, Togoppsett: {row[2]}")
    # Implementer SQL-spørringen og returner resultatene

# d) Søk etter togruter mellom en startstasjon og en sluttstasjon


def search_togruter(conn, startstasjon, sluttstasjon, dato, klokkeslett):
    pass
    # Implementer SQL-spørringen og returner resultatene

# e) Registrer en ny kunde i kunderegisteret


def register_kunde(conn, navn, epost, mobilnummer):
    pass
    # Implementer SQL-spørringen og returner resultatene

# g) Finn ledige billetter for en oppgitt strekning på en ønsket togrute og kjøp billetter


def find_and_buy_billetter(conn, kunde, togrute, reisedato, startstasjon, sluttstasjon, antall_billetter):
    pass
    # Implementer SQL-spørringen og returner resultatene

# h) Finn all informasjon om kjøp for fremtidige reiser for en gitt kunde


def get_kunde_reise_info(conn, kunde_id):
    pass
    # Implementer SQL-spørringen og returner resultatene
