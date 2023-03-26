import sqlite3
import curses

import interface

# h) Finn all informasjon om kjøp for fremtidige reiser for en gitt kunde


def get_kunde_reise_info(conn: sqlite3.Connection, stdscr: curses.window):
    kunde = interface.login(conn, stdscr)

    query = f"""
    SELECT 
    Kunde.Kundenavn,
    Kunde.Epostadresse,
    Kunde.Mobilnummer,
    Kundeordre.Kundeordrenummer,
    Togrute.TogruteID,
    Togrute.Operatør,
    Togruteforekomst.Togruteforekomstdato AS Reisedato,
    Kundeordre.Kjøpsdato,
    Kundeordre.Kjøpstidspunkt,
    Billett.BillettID,
    Billett.Påstigning,
    Billett.Avstigning,
    Billett.Vogn,
    COALESCE(Setebillett.Setenummer, Sengebillett.Sengenummer) AS Sete_eller_Seng,
    CASE 
        WHEN Setebillett.BillettID IS NOT NULL THEN 'Sitte'
        WHEN Sengebillett.BillettID IS NOT NULL THEN 'Sove'
        ELSE NULL
    END AS Sete_eller_Seng_Type
    FROM Kunde
    JOIN Kundeordre ON Kunde.Kundenummer = Kundeordre.Kunde
    JOIN Togruteforekomst ON (Kundeordre.Rute, Kundeordre.Reisedato) = (Togruteforekomst.Rute, Togruteforekomst.Togruteforekomstdato)
    JOIN Togrute ON Kundeordre.Rute = Togrute.TogruteID
    JOIN Billett ON Kundeordre.Kundeordrenummer = Billett.Ordrenummer
    LEFT JOIN Setebillett ON Billett.BillettID = Setebillett.BillettID
    LEFT JOIN Sengebillett ON Billett.BillettID = Sengebillett.BillettID
    LEFT JOIN Vogntype AS SeteVogntype ON Setebillett.Vogntypenavn = SeteVogntype.Vogntypenavn
    LEFT JOIN Vogntype AS SengVogntype ON Sengebillett.Vogntypenavn = SengVogntype.Vogntypenavn
    WHERE Kunde.Kundenummer = ? AND Togruteforekomst.Togruteforekomstdato >= CURRENT_DATE
    ORDER BY Togruteforekomst.Togruteforekomstdato;"""

    cursor = conn.cursor()
    cursor.execute(query, (kunde,))
    rows = cursor.fetchall()
    stdscr.clear()
    interface.check_enough_space(stdscr, len(rows)+4)
    for i, row in enumerate(rows):
        stdscr.addstr(i, 0, str(row))
    stdscr.refresh()
    stdscr.getch()
