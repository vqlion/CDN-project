from datetime import datetime

class CachedFile() : 
    def __init__(self, filename, id):
        self.id = id
        self.filename = filename
        self.last_used = datetime.now()
        self.score = 0

    def change_last_used(self) :
        self.last_used = datetime.now()
        self.update_score()

    def update_score(self) : 
        self.score = self.last_used # here put the right formula 

    def file_to_string(self) : 
        print(f"Cached file no {self.id}")
        print(f"Filename is : {self.filename}")
        print(f"File was last used at : {self.last_used} \n")