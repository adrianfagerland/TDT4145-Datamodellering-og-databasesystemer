import platform
import subprocess

if platform.system() == 'Windows':
    subprocess.check_call(['pip3', 'install', 'windows-curses'])
