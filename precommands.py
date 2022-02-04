import os

def run_pre_commands():
  os.system("python3 -m pip install -U discord.py[voice]")
  os.system("pip3 install pynacl")
