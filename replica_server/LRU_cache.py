from typing import Dict
from cached_file import CachedFile
from time import time

class LRUCache() : 
    def __init__(self):
        self.data : List(CachedFile) = [] # list de CachedFiles
        #self.fill_data_with_existing_files() # implement this function later, or fetch from local json
        self.cache_limit : int = 100 # num of files that can be hold in the cache

    def retreive_file_from_dataset(self, filename : str) -> CachedFile :
        """
            Get the CachedFile object based on the filename string
        """
        for file in self.data : 
            if file.filename == filename : 
                return file
        return None

    def get_file(self, filename : str) : 
        """
            If file is already in the cache call send_directly
            Else call send_and_change_cache
        """
        file = self.retreive_file_from_dataset(filename=filename)
        if file is not None : 
            print("Got the file, sending it")
            self.send_directly(file)
        else : 
            print("Don't have the file, need to fetch it")
            self.send_and_change_cache(file)


    def send_file(self, file : CachedFile) :
        """
            send file back to the user that asked
        """
        return file

    def send_directly(self, file : CachedFile) : 
        """
            send the asked file and update its timestamp 
        """
        file.change_last_used(time.now)


    def send_and_change_cache() : 
        """
            get the asked file from distant server, send it and update the local cache
        """

    def get_file_from_distant_server() : 
        """
            get from distant server
        """

    def update_cache(self, file_to_add) :
        new_file = CachedFile(file_to_add)
        new_file.update_score()
        self.data.add(new_file)
        if self.data.length() < self.cache_limit :
            return 
        self.remove_worst_score()
    
    def remove_worst_score() :
        """"
            implement worst score removal 
        """
