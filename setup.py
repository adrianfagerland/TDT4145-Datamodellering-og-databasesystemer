import platform
import subprocess

if platform.system() == 'Windows':
    try:
        import windows_curses as curses
    except ImportError:
        subprocess.check_call(['pip', 'install', 'windows-curses'])
        import windows_curses as curses
else:
    try:
        import curses
    except ImportError:
        subprocess.check_call(['pip', 'install', 'curses'])
        import curses

try:
    import sqlite3
except ImportError:
    subprocess.check_call(['pip', 'install', 'pysqlite3'])
    import sqlite3

# Rest of your code using curses and sqlite3
