from pprint import pprint
from shutil import rmtree
from pathlib import Path
import json

from Server.user import User

# USER
def user_info(user, args, flags):
    if("-h" or "--help") in flags:
        print(
            "[args...] = None\n"
            "Prints the info (rating, lastonline, etc.) of the user"
        )
        return
    pprint(user.info)

def user_rating(user, args, flags):
    if ("-h" or "--help") in flags:
        print(
            "[args...] = None\n"
            "Prints the rating-data (contestID, oldrating, etc.) of the user"
        )
        return
    pprint(user.rating)

def user_help(user, args, flags):
    print(
        "user <fn>[args...] [--flags] [-sfalgs]\n"
        "       fn      ::  info(None), rating(None)\n" 
        "       flags   ::  --help\n"
        "       sflags  ::  -h"
    )

def user_invalid():
    print("Please type \"user -h\" for help")


# Clear
def clear_screen(user, args, flags):
    pass

def clear_cache(user, args, flags):
    rmtree(user.pathDB)
    print("Cleared Cache!!")

def clear_help(user, args, flags):
    print(
        "clear <type>[args...] [--flags] [-sflags]\n"
        "       type    ::  screen(None), cache(None)\n"
        "       flags   ::  --help\n"
        "       sflags  ::  -h"
    )

def clear_invalid():
    print("Please type \"clear -h\" for help")


# Export
def export_json(user : User, args, flags : dict):
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

def export_csv(user, args, flags):
    pass

def export_help(user, args, flags):
    print(
        "export <type>[args...] [--flags] [-sflags]\n"
        "       type    ::  json(path), csv(path)\n"
        "       flags   ::  --help, --verbose, --indent, --path\n"
        "       sflags  ::  -h, -v"
    )

def export_invalid():
    pass


# Invalid
def invalid():
    print("Please enter a valid command")
    

# End
def end():
    exit(1)