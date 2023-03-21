import platform
import subprocess

if platform.system() == 'Windows':
    subprocess.check_call(['pip3', 'install', 'windows-curses'])
else:
    subprocess.check_call(['pip3', 'install', 'curses'])

subprocess.check_call(['pip3', 'install', 'pysqlite3'])

# Rest of your code using curses and sqlite3
