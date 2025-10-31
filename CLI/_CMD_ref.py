# This file is just a reference to see all the functions and is not the actual
# source, that is in to functions.py

from CLI.functions import *

# Protocol:
#    - Every 'main' cmd must implement "help", "invalid" methods
#    - command = main sub [args...] [--flags] [-shortflags]
CMD = {
    "user" : {
        "info" : user_info,
        "rating" : user_rating,
        "compare" : user_compare,
        
        "help" : user_help,
        "invalid" : user_invalid,
    },
    "clear" : {
        "screen" : clear_screen,
        "cache" : clear_cache,
        
        "help" : clear_help,
        "invalid" : clear_invalid,
    },
    "export" : {
        "json" : export_json,
        "csv" : export_csv,
    
        "help" : export_help,
        "invalid" : export_invalid,
    },
    
    # General (single param fn)
    "help" : gen_help,
    "invalid" : invalid,
    "quit" : end,
    "q" : end,
}

