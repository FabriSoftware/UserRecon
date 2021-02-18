import lib.connection as connection
import lib.utils as utils
from colorama import Fore


header = """ 

    ██╗   ██╗███████╗███████╗██████╗ ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
    ██║   ██║██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
    ██║   ██║███████╗█████╗  ██████╔╝██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
    ██║   ██║╚════██║██╔══╝  ██╔══██╗██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
    ╚██████╔╝███████║███████╗██║  ██║██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
    ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                            
 """
    
def main():
    utils.clear()
    if utils.isNew():
     print(Fore.GREEN+header)
     print("\t\tAuthor: @fabrisoftware | Fabriziodeveloper")
     print("\t\tGitHub: https://github.com/FabriSoftware/UserRecon/")
     print("\t\tTwitter: @Fabritutoriale_\n")
     utils.configure()
    else:
     utils.clear()
     print("["+Fore.YELLOW+"*"+Fore.RESET+"] loading config saved...")
     connected()


def connected():
    config = utils.getCnf()
    
    result = connection.connection(config["host"], config["port"], config["password"])
        
    if not result:
        print("["+Fore.RED+"X"+Fore.RESET+"] incorrect password")
        exit(1)

    while True:
     request = user_input("> ")
     if request == "exit" or request == "quit":
      print("["+Fore.GREEN+"~"+Fore.RESET+"] bye, bye")
      result.close()
      break
     
     if request == "stop":
         connection.send_command(result, "stop")
         print("["+Fore.GREEN+"~"+Fore.RESET+"] the remote server has been stopped")
         result.close()
         break

     response = connection.send_command(result, request)
     print(response)


def user_input(prompt):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("["+Fore.GREEN+"-"+Fore.RESET+"] press control-c again to quit")
    return input(prompt) 


if __name__ == '__main__':
    main()