from pprint import pprint
from shutil import rmtree
from pathlib import Path
import json

from Server.user import User, _info

# USER
def user_info(user : User, args : list[str], flags : dict[str, str]):
    if("-h" or "--help") in flags:
        print(
            "[args...] = None\n"
            "Prints the info (rating, lastonline, etc.) of the user"
        )
        return
    pprint(user.info)
    print("Formatted ouptut will be added!")

def user_rating(user : User, args : list[str], flags : dict[str, str]):
    if ("-h" or "--help") in flags:
        print(
            "[args...] = None\n"
            "Prints the rating-data (contestID, oldrating, etc.) of the user"
        )
        return
    pprint(user.rating)
    print("Formatted output will be added!")

def user_compare(user : User, args : list[str], flags : dict[str, str]):
    if len(args)==0:
        print("Please enter valid arguments! Type user compare -h for help")
    if len(args)==1 :
        if args[0]=="-h" or args[0]=="--help":
            print("Input a handle of a user with whom you want to be compared with")
        else:
            other = User(args[0], False)
            
            if(not other.success) : 
                print(f"Maybe check the username?")
                return
            
            print("─" * 60)
            print(
                f"{user.handle} ({user.info.rating}, {user.info.rank})"
                " vs "
                f"{other.handle} ({other.info.rating}, {other.info.rating})"
            )
            print("--More trackers will be added!--")
            print("─" * 60)
            
            rmtree(other.pathDB)
    

def user_help(user : User, args : list[str], flags : dict[str, str]):
    print(
        "user <fn>[args...] [--flags] [-sfalgs]\n"
        "       fn      ::  info(None), rating(None)\n" 
        "       flags   ::  --help\n"
        "       sflags  ::  -h"
    )

def user_invalid():
    print("Please type \"user -h\" for help")


# Clear
def clear_screen(user : User, args : list[str], flags : dict[str, str]):
    print("Not yet added!")

def clear_cache(user : User, args : list[str], flags : dict[str, str]):
    rmtree(user.pathDB)
    print("Cleared Cache!!")

def clear_help(user : User, args : list[str], flags : dict[str, str]):
    print(
        "clear <type>[args...] [--flags] [-sflags]\n"
        "       type    ::  screen(None), cache(None)\n"
        "       flags   ::  --help\n"
        "       sflags  ::  -h"
    )

def clear_invalid():
    print("Please type \"clear -h\" for help")


# Export
def export_json(user : User, args : list[str], flags : dict[str, str]):
    if Path(flags.get("--path", "_")).exists():
        
        info_path = Path(flags["--path"], "info.json")
        rating_path = Path(flags["--path"], "rating.json")
        
        with open(info_path, "w") as f:
            json.dump(user.info, f, indent=flags.get("--indent", 0))
        with open(rating_path, "w") as f:
            json.dump(user.rating, f, indent=flags.get("--indent", 0))
        
        if ("-v" or "--verbose") in flags:
            print("Successfully written to files:\n"
                 f" -> {info_path}\n"
                 f" -> {rating_path}"
            )
    else : 
        print(
            "The specified directory doesn't exist!\n"
            "A valid directory is required to generate the necessary files."
        )

def export_csv(user : User, args : list[str], flags : dict[str, str]):
    print("Feature not yet available!")

def export_help(user : User, args : list[str], flags : dict[str, str]):
    print(
        "export <type>[args...] [--flags] [-sflags]\n"
        "       type    ::  json(path), csv(path)\n"
        "       flags   ::  --help, --verbose, --indent, --path\n"
        "       sflags  ::  -h, -v"
    )

def export_invalid():
    pass


# Help
def gen_help():
    for x in CMD.keys():
        print("-> " + x.upper())


# Invalid
def invalid():
    print("Please enter a valid command")
    

# End
def end():
    exit(1)

# Protocol:
#    - Every 'main' cmd must implement "help", "invalid" methods
#    - command = main sub [args...] [--flags] [-shortflags]
CMD = {
    "user" : {
        "info" : user_info,
        "rating" : user_rating,
        "compare" : user_compare,
        
        "--help" : user_help,
        "-h" : user_help,
        "invalid" : user_invalid,
    },
    "clear" : {
        "screen" : clear_screen,
        "cache" : clear_cache,
        
        "--help" : clear_help,
        "-h" : clear_help,        
        "invalid" : clear_invalid,
    },
    "export" : {
        "json" : export_json,
        "csv" : export_csv,
    
        "--help" : export_help,
        "-h" : export_help,
        "invalid" : export_invalid,
    },
    
    # General (single param fn)
    "help" : gen_help,
    "invalid" : invalid,
    "quit" : end,
    "q" : end,
}
