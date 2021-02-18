import os
import sys
import main
import json
from colorama import Fore

def clear():
    if os.name == 'nt':
      _ = os.system("cls")
    else:
      _ = os.system('clear')


def isNew():
   if not os.path.isfile("config.json"):
       return True
   else:
       return False

def setCnf(host, port, password):
     with open("config.json", "w+") as file:
      json.dump({"host": host, "port": port, "password": password}, file)

def getCnf():
     with open("config.json", "r") as file:
      config = json.load(file)
      return config
    
def configure():
  host = input("["+Fore.GREEN+"+"+Fore.RESET+"] set hostname (127.0.0.1): ")
  if not host:
      host = "127.0.0.1"

  port = input("["+Fore.GREEN+"+"+Fore.RESET+"] set port (19132): ")
  if not port:
      port = 19132

  password = input("["+Fore.GREEN+"+"+Fore.RESET+"] type rcon password: ")
  if not password:
      print("["+Fore.RED+"X"+Fore.RESET+"] please insert password!")
      exit(1)
  setCnf(host, port, password)
  clear()
  main.connected()