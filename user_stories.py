from datetime import datetime, timedelta
import sqlite3

from brukerhistorier import c, d, e, g, h


def handle(conn: sqlite3.Connection, choice, stdscr):
    functions = {1: c.get_togruter_by_stasjon_and_day, 2: d.search_togruter,
                 3: e.register_kunde, 4: g.find_and_buy_billetter, 5: h.get_kunde_reise_info}

    functions[choice](conn, stdscr)
