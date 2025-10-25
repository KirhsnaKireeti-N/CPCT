from enum import Flag, auto
from pprint import pprint

from Server.user import User

class CMD(Flag):
    # General
    INVALID = auto(),
    CONTINUE = auto(),
    HELP = auto(),
    UPDATE = auto(),
    QUIT = auto(),
    
    # Low-Level
    INFO = auto(),
    RATING = auto()
    
    # High-Level
    OVERVIEW = auto(),
    
    
    def toCMD(cmd : str) -> CMD:
        if(cmd == "") : return CMD.CONTINUE
        try:
            return CMD[cmd.upper()]
        except KeyError:
            return CMD.INVALID
    

inp = ">>>"
def start() :
    quit = False
    handle = None
    while not(quit) :
        while handle==None:
            try:
                handle = input(f"{inp} Enter your codeforces handle: ")
            except KeyboardInterrupt:
                print("\n:(")
                exit(-1)

        _main(User(handle, True))


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
            print(default)
        case CMD.INVALID:
            print("Invalid INPUT! Type HELP for help!")