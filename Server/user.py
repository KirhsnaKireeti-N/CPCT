from Server.__init__ import *

import requests
from datetime import datetime
import json

# SERVER
class User:
    _api : dict = {
        "info"    : "https://codeforces.com/api/user.info",
        "rating"  : "https://codeforces.com/api/user.rating"
    }
    
    # var => str:handle, dict:info, dict:rating
    
    def __init__(self, handle : str, format_flag : bool = False):
        self.handle = handle
        
        response = requests.get(
            self._api["info"], 
            params={"handles": self.handle}
        )
        self.info = dict(self._check(response)[0])
        
        response = requests.get(
            self._api["rating"],
            params={"handle" : self.handle}
        )
        self.rating = self._check(response) # Also initializes self.rating
        
        if(format_flag) : 
            self._format()
            self.addDB()

    
    # DataBase Stuff
    def addDB(user : User) :
        path = DATABASE_PATH / user.handle
        path.mkdir(parents=True, exist_ok=True)
        
        with open(path / "info.json", "w") as f:
            #json.dump(user.info, f)
            json.dump(user.info, f, indent=4)
        with open(path / "rating.json", "w") as f:
            #json.dump(user.info, f)
            json.dump(user.rating, f, indent=4)
    
    
    def _format(self):
        # Formatting info:
        self.info.pop("contribution")
        self.info.pop("friendOfCount")
        self.info.pop("titlePhoto")
        self.info.pop("handle")
        self.info.pop("avatar")
        self.info.pop("registrationTimeSeconds")
        self.info["lastOnlineTime"] = str(datetime.fromtimestamp(
            self.info.pop("lastOnlineTimeSeconds")))
        
        # Formatting rating
        for contest in self.rating:
            contest.pop("handle")
            contest.pop("ratingUpdateTimeSeconds")
        

    
    def _check(self, response : requests.Response) -> dict :
            if(response.ok) : 
                data = dict(response.json())
            else :
                print(f"{response.status_code} : IDK WHY")
                exit(-1)
            if(data["status"]=="FAILED") : 
                raise RuntimeError(f"API call failed: {data.get('comment', 'Unknown error')}")
            
            return data["result"]