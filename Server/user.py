from Server.__init__ import *

import requests
import json
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class _info:
    handle : str
    rank : str
    rating : int
    maxRank : str
    maxRating : int
    lastOnline : str
    organization : str = None
    

@dataclass(frozen=True)
class _rating:
    contestId : int
    contestName : str
    rank : int
    oldRating : int
    newRating : int


# SERVER
class User:
    _api : dict = {
        "info"    : "https://codeforces.com/api/user.info",
        "rating"  : "https://codeforces.com/api/user.rating"
    }
    
    # var => str:handle, dict:info, dict:rating
    
    def __init__(self, handle : str, break_on_req_fail : bool):
        self.handle = handle
        self.break_on_fail = break_on_req_fail
        
        DATABASE_PATH.mkdir(parents=True, exist_ok=True)
        self.pathDB = DATABASE_PATH / self.handle
        
        # Data : "info", "rating"
        self.success = self.getData()

    
    # Get Data
    def getData(self) -> bool :
        if(self._fromDB()) : 
            self._format()
            return True
        response = requests.get(
            self._api["info"], 
            params={"handles": self.handle}
        )
        check = list(self._check(response))
        if(check==None) :
            return False
        self._info = check
        
        response = requests.get(
            self._api["rating"],
            params={"handle" : self.handle}
        )
        self._rating = list[dict](self._check(response))
        
        self._format()
        self._addDB()
        
        return True
    
    
    # Add a new user to DataBase
    def _addDB(self) :
        self.pathDB.mkdir(parents=True, exist_ok=True)
        with open(self.pathDB / "info.json", "w") as f:
            #json.dump(user.info, f)
            json.dump(self._info, f, indent=4)
        with open(self.pathDB / "rating.json", "w") as f:
            #json.dump(user.info, f)
            json.dump(self._rating, f, indent=4)
    
    
    # If user exists, collect data from DataBase
    def _fromDB(self) -> bool:
        if self.pathDB.exists() :
            with open(self.pathDB / "info.json", "r") as f:
                self._info = json.load(f)
            with open(self.pathDB / "rating.json", "r") as f:
                self._rating = json.load(f)
            return True
        else :
            return False
    
    # Format
    def _format(self):
        # Formatting info:
        self._info = dict(self._info[0])
        self._info.pop("email", 0)
        self._info.pop("vkld", 0)
        self._info.pop("openID", 0)
        self._info.pop("firstName", 0)
        self._info.pop("lastName", 0)
        self._info.pop("country", 0)
        self._info.pop("city", 0)
        self._info.pop("contribution", 0)
        self._info.pop("friendOfCount", 0)
        self._info.pop("registrationTimeSeconds", 0)
        self._info.pop("avatar", 0)
        self._info.pop("titlePhoto", 0)
        self._info["lastOnline"] = str(datetime.fromtimestamp(
            self._info.pop("lastOnlineTimeSeconds")))
        self.info = _info(**self._info)
        self._info = [self._info]
        
        # Formatting rating
        self.rating = []
        for contest in self._rating:
            contest.pop("handle", 0)
            contest.pop("ratingUpdateTimeSeconds", 0)
            self.rating.append(_rating(**contest))
        

    
    def _check(self, response : requests.Response) -> list :
            if(response.ok) : 
                data = dict(response.json())
            else :
                if self.break_on_fail : 
                    print(f"{response.status_code} : Maybe check the username?")
                    exit(-1)
                else :
                    print(f"StatusCode : {response.status_code}")
                    return None
            if(data["status"]=="FAILED") : 
                raise RuntimeError(f"API call failed: {data.get('comment', 'Unknown error')}")
            
            return data["result"]