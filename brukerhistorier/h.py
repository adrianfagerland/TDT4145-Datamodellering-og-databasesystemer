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
    COUNT(*) AS Antall_Billetter,
    CASE 
        WHEN Sengebillett.BillettID IS NOT NULL AND Setebillett.BillettID IS NOT NULL THEN 'Sove og Sitte'
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
    if rows:
        col1_w = len('Ordrenr.') + 1
        col2_w = max(
            max(len(row[2]), len('TogruteID')) for row in rows) + 3
        col3_w = max(
            max(len(row[3]), len('Operatør')) for row in rows) + 3
        col4_w = max(
            max(len(row[4]), len('Reisedato')) for row in rows) + 3
        col5_w = max(
            max(len(row[5]), len('Påstigning')) for row in rows) + 3
        col6_w = max(
            max(len(row[6]), len('Avstigning')) for row in rows) + 3
        col7_w = len('Vogn') + 3
        col8_w = len('Ant. bil.') + 3
        col9_w = max(
            max(len(row[9]), len('Billettype')) for row in rows) + 3

        header = f"{'Ordrenr.':<{col1_w}}{'TogruteID':<{col2_w}}{'Operatør':<{col3_w}}{'Reisedato':<{col4_w}}{'Påstigning':<{col5_w}}{'Avstigning':<{col6_w}}{'Vogn':<{col7_w}}{'Ant. bil.':<{col8_w}}{'Billettype':<{col9_w}}"

        stdscr.addstr(2, 0, header, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(3, 0, "-" * (len(header)))

    for idx, row in enumerate(rows):
        result_row = f"{row[1]:<{col1_w}}{row[2]:<{col2_w}}{row[3]:<{col3_w}}{row[4]:<{col4_w}}{row[5]:<{col5_w}}{row[6]:<{col6_w}}{row[7]:<{col7_w}}{row[8]:<{col8_w}}{row[9]:<{col9_w}}"
        stdscr.addstr(idx + 4, 0, f"{result_row}", curses.color_pair(3))
    stdscr.refresh()
    stdscr.getch()
