from CLI._functions import *

# Protocol:
#    - Every 'main' cmd must implement "help", "invalid" methods
CMD = {
    "user" : {
        "info" : user_info,
        "rating" : user_rating,
        
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
    "invalid" : invalid,
    "quit" : end,
    "q" : end,
}

