import sqlite3
import curses

import interface

# c) Hent togruter som er innom en gitt stasjon på en gitt ukedag


def get_togruter_by_stasjon_and_day(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    stasjon = interface.velg_avreisestasjon(cursor, stdscr)

    ukedag_prompt = "Velg ukedag: "
    ukedager = ["Mandag", "Tirsdag", "Onsdag",
                "Torsdag", "Fredag", "Lørdag", "Søndag"]
    ukedag = interface.selectable_menu(stdscr, ukedag_prompt, ukedager)

    query = f"""
        SELECT t1.TogruteID, t1.Stasjon AS EndStasjon, t2.Ankomst AS CurrentStasjonAnkomst, t2.Avgang AS CurrentStasjonAvgang
        FROM Togrutetabell t1
        INNER JOIN Togrutetabell t2 ON t1.TogruteID = t2.TogruteID
        WHERE t1.Stasjonnummer = (
            SELECT MAX(Stasjonnummer)
            FROM Togrutetabell
            WHERE TogruteID = t1.TogruteID
        )
        AND LOWER(t2.Stasjon) = LOWER(?)
        AND ((EXISTS (
            SELECT 1
            FROM Togrute
            WHERE TogruteID = t1.TogruteID AND {ukedag} = 1
        ) AND SUBSTR(t2.avgang, -2) != "+1") OR (EXISTS (
            SELECT 1
            FROM Togrute
            WHERE TogruteID = t1.TogruteID AND {ukedager[ukedager.index(ukedag)-1]} = 1
        ) AND SUBSTR(t2.avgang, -2) == "+1")
        )
    """
    cursor.execute(query, (stasjon,))

    # Skriv ut resultatene
    stdscr.clear()
    rows = cursor.fetchall()

    stdscr.addstr(0, 0, f"Togruter fra {stasjon} på {ukedag.lower()}er.", curses.color_pair(
        2) | curses.A_BOLD)
    stdscr.refresh()

    if rows:
        togrute_id_width = max(
            max(len(row[0]), len('TogruteID')) for row in rows) + 6
        endestasjon_width = max(max(len(row[1]), len(
            stasjon), len('Endestasjon')) for row in rows) + 6
        avgang_ankomst_width = max(max(len(row[2]), len(
            row[3]), len('Avgang')) for row in rows)

        header = f"{'TogruteID':<{togrute_id_width}}{'Endestasjon':<{endestasjon_width}}{'Avgang':<{avgang_ankomst_width}}"
        stdscr.addstr(2, 0, header, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(3, 0, "-" * (len(header)))
    else:
        stdscr.addstr(2, 0, "Ingen resultater funnet",
                      curses.color_pair(1) | curses.A_BOLD)

    for idx, row in enumerate(rows):
        result_row = f"{row[0]:<{togrute_id_width}}{row[1]:<{endestasjon_width}}{row[3][:5]:<{avgang_ankomst_width}}"
        stdscr.addstr(idx + 4, 0, result_row, curses.color_pair(3))

    stdscr.refresh()

    stdscr.getch()  # Wait for user to press a key before returning to the menu
