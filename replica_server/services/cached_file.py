from datetime import datetime
from enum import Enum

class Origin(Enum):
    STATIC = "static"
    CACHED = "contents"

class CachedFile() : 
    def __init__(self, filename, id, origin):
        if not isinstance(origin, Origin):
            raise ValueError("Origin must be an instance of Origin Enum")
        
        self.id = id
        self.filename = filename
        self.last_used = datetime.now()
        self.origin = origin
        self.score = 0

    def change_last_used(self) :
        self.last_used = datetime.now()
        self.update_score()

    def update_score(self) : 
        self.score = self.last_used # here put the right formula 

    def file_to_string(self) : 
        print(f"Cached file no {self.id}")
        print(f"Filename is : {self.filename}")
        print(f"File has origin : {self.origin}")
        print(f"File was last used at : {self.last_used} \n")