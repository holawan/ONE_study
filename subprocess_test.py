#utils.py
import subprocess
import sys


cmd = "df -h"
subprocess.Popen(cmd, shell=True)

cmd = "df -a"
subprocess.Popen(cmd, shell=True)