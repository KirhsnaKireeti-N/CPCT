from enum import Enum, auto
from pprint import pprint

from Server.user import User

class CMD(Enum):
    # General
    HELP = auto(),
    QUIT = auto(),
    UPDATE = auto(),
    INVALID = auto(),
    CONTINUE = auto(),

    # Low-Level
    INFO = auto(),
    RATING = auto()
    
    # High-Level
    OVERVIEW = auto(),
    
    
    def toCMD(cmd : str) -> CMD:
        if(cmd == "") : return CMD.CONTINUE
        if(cmd == "q" or cmd == "Q") : return CMD.QUIT
        try:
            return CMD[cmd.upper()]
        except KeyError:
            return CMD.INVALID
    

inp = ">>>"
def start() :
    handle = None
    while handle==None:
        try:
            handle = input(f"{inp} Enter your codeforces handle: ")
        except KeyboardInterrupt:
            print("\n:(")
            exit(-1)
    user = User(handle)
    while 1 :
        _main(user)


def _main(user : User) :
    try:
        command = CMD.toCMD(input(f"{inp} "))
    except KeyboardInterrupt:
        print("\n:(")
        exit(-1)

    default = "Feature not yet available"
    
    match command:
        # Low-Level
        case CMD.INFO:
            pprint(user.info)
        case CMD.RATING:
            pprint(user.rating)
        
        # High-Level
        case CMD.OVERVIEW:
            pprint(user.info)
            pprint(user.rating)
        
        # General
        case CMD.QUIT:
            print("GO WORK YOU IDIOT!")
            exit(-1)
        case CMD.HELP:
            for name, member in CMD.__members__.items():
                print(name)
        case CMD.UPDATE:
            user.getData()
        case CMD.INVALID:
            print("Invalid INPUT! Type HELP for help!")
        case CMD.CONTINUE:
            pass