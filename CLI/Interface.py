from enum import Enum, auto
from pprint import pprint

from Server.user import User    
from CLI.CMD import *

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
        command = input(f"{inp} ")
        if(command==None) : return
    except KeyboardInterrupt:
        print("\n:(")
        exit(-1)
        
    # command = main sub [args...] [--flags] [-shortflags]
    command = command.strip().lower().split()
    
    n = len(command)
    args = []
    flags = {}
    if(n==1) :
        main = command[0]
        if(main not in CMD) : 
            CMD["invalid"]()
        else : 
            CMD[main]()
    elif(n==2) :
        main = command[0]
        if(main not in CMD) : 
            CMD["invalid"]()
            return
        sub = command[1]
        if sub not in CMD[main] : 
            CMD[main]["invalid"]()
            return
        CMD[main][sub](user, args, flags)
    else :
        main = command[0]
        if(main not in CMD) : 
            CMD["invalid"]()
            return
        
        i = 1
        first = True
        while i < len(command):
            part = command[i]
            if part.startswith('-'):
                flags[part] = True
            if part.startswith('--'):
                if '=' in part:
                    key, value = part.split("=")
                    print(key, value)
                    flags[key] = value
                else:
                    flags[part] = True
            else:
                if(first) :
                    sub = part
                    first = False
                else:
                    args.append(part)
            i+=1
        CMD[main][sub](user, args, flags)

