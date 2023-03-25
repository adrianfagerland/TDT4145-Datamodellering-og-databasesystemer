import sqlite3
import curses

import interface

# g) Finn ledige billetter for en oppgitt strekning på en ønsket togrute og kjøp billetter


def find_and_buy_billetter(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    # kunde = interface.find_kundenummer(cursor, stdscr) #implementert
    togrute = interface.input_togrute(cursor, stdscr)  # implementert
    reisedato = interface.input_reisedato(cursor, stdscr)  # implementert
    startstasjon = interface.input_startstasjon(cursor, stdscr, togrute)
    sluttstasjon = interface.input_sluttstasjon(
        cursor, stdscr, togrute, startstasjon)
    billettID = interface.make_billettID(cursor)  # implementert
    kundeordrenummer = interface.make_kundeordrenummer(cursor)  # implementert
    kjopsdato = interface.get_kjopsdato()  # implementert
    billetttype = interface.velg_billettype(cursor, stdscr)
    antallBilletter = interface.input_billetter(cursor, stdscr)  # implementert
    if billetttype == "sete":
        cursor.execute("""
        WITH Sittevogner AS (
        SELECT Vognnummer, AvType
        FROM Vogn
        WHERE Togoppsett = (
            SELECT Togoppsett
            FROM Togrute
            WHERE TogruteID = ? 
        )
        AND AvType IN (
            SELECT Vogntypenavn
            FROM Vogntype
            WHERE Type = 'Sitte'
        )
    ),
    OpptatteSeter AS (
        SELECT Setenummer, Vogntypenavn, Vognnummer
        FROM Setebillett
        JOIN Billett ON Setebillett.BillettID = Billett.BillettID
        WHERE Ordrenummer IN (
            SELECT Kundeordrenummer
            FROM Kundeordre
            WHERE Rute = ? AND Reisedato = ? AND 
        ) AND (
            (Billett.Påstigning < ? AND Billett.Avstigning > ?)
            OR (Billett.Påstigning >= ? AND Billett.Påstigning < ?)
        )
    ),
    LedigeSeter AS (
        SELECT Setenummer, Sittetypenavn, Radnummer, Vognnummer
        FROM Sete
        JOIN Sittevogner ON Sete.Sittetypenavn = Sittevogner.AvType
        WHERE (Setenummer, Sittetypenavn) NOT IN (
            SELECT Setenummer, Vogntypenavn
            FROM OpptatteSeter
        )
    )
    SELECT * FROM LedigeSeter;
    """,
                       (togrute, togrute, reisedato, startstasjon, startstasjon, startstasjon, sluttstasjon))
    if billetttype == "seng":
        cursor.execute("""
        WITH Sengevogner AS (
        SELECT Vognnummer, AvType
        FROM Vogn
        WHERE Togoppsett = (
            SELECT Togoppsett
            FROM Togrute
            WHERE TogruteID = ?
        )
        AND AvType IN (
            SELECT Vogntypenavn
            FROM Vogntype
            WHERE Type = 'Senge'
        )
    ),
    OpptatteKupe AS (
        SELECT Kupenr, Vognnummer
        FROM Sengeplassbillett
        JOIN Billett ON Sengeplassbillett.BillettID = Billett.BillettID
        WHERE Ordrenummer IN (
            SELECT Kundeordrenummer
            FROM Kundeordre
            WHERE Rute = ? AND Reisedato = ? AND Vogn
        )
    ),
    LedigeSenge AS (
        SELECT Sengeplassnummer, Sengetypenavn, Kupenr, Vognnummer
        FROM Sengeplass
        JOIN Sengevogner ON Sengeplass.Sengetypenavn = Sengevogner.AvType
        WHERE (Kupenr, Vognnummer) NOT IN (
            SELECT Kupenr, Vognnummer
            FROM OpptatteKupe
        )
    )
    SELECT * FROM LedigeSenge;
    """)
    tilgjengelig = [row[0] for row in cursor.fetchall()]
    prompt = "Her er " + str(antallBilletter) + " tilgjengelige billetter:"
    for i in range(antallBilletter):
        prompt += "\nTest" + str(tilgjengelig[1])

    stdscr.getch()  # Wait for user to press a key before returning to the menu
