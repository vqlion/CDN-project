class CachedFile() : 
    def __init__(self, filename):
        self.filename = filename
        self.last_used = 0
        self.score = 0

    def change_last_used(self, new_timestamp) :
        self.last_used = new_timestamp
        self.update_score()

    def update_score(self) : 
        self.score = self.last_used # here put the right formula 