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
    
    def __init__(self, handle : str):
        self.handle = handle
        
        self.pathDB = DATABASE_PATH / self.handle
        self.pathDB.mkdir(parents=True, exist_ok=True)
        
        # Data : "info", "rating"
        if(self._fromDB()) : return
        self.getData()

    
    # Get Data
    def getData(self) :
        response = requests.get(
            self._api["info"], 
            params={"handles": self.handle}
        )
        self.info = dict(self._check(response)[0])
        
        response = requests.get(
            self._api["rating"],
            params={"handle" : self.handle}
        )
        self.rating = self._check(response)
        
        self._format()
        self._addDB()
    
    # DataBase Stuff
    def _addDB(self) :
        with open(self.pathDB / "info.json", "w") as f:
            #json.dump(user.info, f)
            json.dump(self.info, f, indent=4)
        with open(self.pathDB / "rating.json", "w") as f:
            #json.dump(user.info, f)
            json.dump(self.rating, f, indent=4)
    
    
    def _fromDB(self) -> bool:
        if self.pathDB.exists() :
            with open(self.pathDB / "info.json", "r") as f:
                self.info = json.load(f)[0]
            with open(self.pathDB / "rating.json", "r") as f:
                self.rating = json.load(f)
            return True
        else :
            return False
    
    # Format
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