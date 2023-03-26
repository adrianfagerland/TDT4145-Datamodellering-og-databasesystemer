import sqlite3
import curses

import interface

# h) Finn all informasjon om kjøp for fremtidige reiser for en gitt kunde


def get_kunde_reise_info(conn: sqlite3.Connection, stdscr: curses.window):
    kunde = interface.login(conn, stdscr)

    query = f"""
    SELECT 
    Kunde.Kundenavn,
    Kundeordre.Kundeordrenummer,
    Togrute.TogruteID,
    Togrute.Operatør,
    Togruteforekomst.Togruteforekomstdato AS Reisedato,
    Billett.Påstigning,
    Billett.Avstigning,
    Billett.Vogn,
    COALESCE(Setebillett.Setenummer, Sengebillett.Sengenummer) AS Sete_eller_Seng,
    COUNT(*) AS Antall_Billetter,
    CASE 
        WHEN Sengebillett.BillettID IS NOT NULL THEN 'Sove'
        WHEN Setebillett.BillettID IS NOT NULL THEN 'Sitte'
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
    GROUP BY Kundeordre.Kundeordrenummer
    ORDER BY Togruteforekomst.Togruteforekomstdato;"""

    cursor = conn.cursor()
    cursor.execute(query, (kunde,))
    rows = cursor.fetchall()
    stdscr.clear()
    interface.check_enough_space(stdscr, len(rows)+4)
    stdscr.addstr(0, 0, f"Informasjon om {rows[0][0]} sine fremtidige kjøp:", curses.color_pair(
        2) | curses.A_BOLD)
    stdscr.refresh()
    # if rows:
    #     togrute_id_width = max(
    #         max(len(row[0]), len('TogruteID')) for row in rows) + 6
    #     endestasjon_width = max(
    #         max(len(row[1]), len('Endestasjon')) for row in rows) + 6
    #     avgang_ankomst_width = 10

    #     header = f"{'TogruteID':<{togrute_id_width}}{'Endestasjon':<{endestasjon_width}}{'Avgang':<{avgang_ankomst_width}}"
    #     stdscr.addstr(2, 0, header, curses.color_pair(1) | curses.A_BOLD)
    #     stdscr.addstr(3, 0, "-" * (len(header)))

    for idx, row in enumerate(rows):
        result_row = row
        stdscr.addstr(idx + 4, 0, f"{result_row}", curses.color_pair(3))
    stdscr.refresh()
    stdscr.getch()
