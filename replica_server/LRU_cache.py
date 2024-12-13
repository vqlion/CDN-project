from typing import Dict, List
from cached_file import CachedFile
from time import time, sleep
import requests
from datetime import datetime
from os import walk
import os 
from PIL import Image
import shutil

"""
    TO-DO : 

    - Pb quand on demande deux fois une default image, y'en a quand meme une qui est supprimée du côté du replica
    - add logging ? 
    - add error handling ? 
    - get current files via a json instead of data dict ? 
    - replace user and server interactions with api calls
    - pb de default.png dans main_server (see readme)
    - pb de taille de cache (n-1 ?)
""" 

class LRUCache() : 
    def __init__(self):
        self.data : List(CachedFile) = [] # list de CachedFiles
        self.fill_data_with_existing_files()
        self.cache_limit : int = 5 # num of files that can be hold in the cache


    def retreive_file_from_dataset(self, filename : str) -> CachedFile :
        """
            Get the CachedFile object based on the filename string
        """
        for file in self.data :
            if file.filename == filename :
                return file
        return None
    

    def fill_data_with_existing_files(self) :
        """
            Used only in init : lookup what files are in the content dir and populates self.data accordingly
        """
        path = "contents"
        filenames = next(walk(path), (None, None, []))[2]  # [] if no file
        for id, filename in enumerate(filenames) : 
            new_file = CachedFile(filename=filename, id=id)
            self.data.append(new_file)
        self.pretty_print("Cache state at init :")
        self.cache_to_string()
    

    def cache_to_string(self) : 
        """
            To string method to print whole content of the cache
        """
        for file in self.data : 
            file.file_to_string()


    def get_file(self, filename) :
        """
            If file is already in the cache call send_directly
            Else call send_and_change_cache
        """
        self.pretty_print(f"Got asked for file : {filename}")
        file = self.retreive_file_from_dataset(filename=filename)
        if file is not None :
            self.pretty_print("This file is present in my cache")
            self.send_directly(file)
        else : 
            self.pretty_print("Don't have the file, need to fetch it")
            self.send_and_change_cache(filename)


    def send_file(self, file : CachedFile) :
        """
            send file back to the user that asked
        """
        self.pretty_print(f"SENDING FILE :")
        file.file_to_string()

        """image = Image.open(image_path)
        image.show()
        sleep(0.5)"""


    def send_directly(self, file : CachedFile) :
        """
            send the asked file and update its timestamp 
        """
        file.change_last_used()
        self.send_file(file)


    def send_and_change_cache(self, filename : str) :
        """
            get the asked file from distant server, send it and update the local cache
        """
        new_file = self.get_file_from_distant_server(filename)
        if new_file is None : 
            print("File retreival was impossible, no one has it. Sorry owo")
        new_file = CachedFile(new_file, self.get_next_id())
        self.update_cache(new_file)
        self.send_file(new_file)


    def get_file_from_distant_server_test(self, new_filename : str) :
        """
            get from distant server locally for tests (without any api calls)
        """
        path = "distant_server_contents"
        filenames = next(walk(path), (None, None, []))[2]  # [] if no file
        for filename in filenames : 
            if filename == new_filename :
                src = "distant_server_contents/" + filename
                dst = "contents/" + filename
                shutil.copyfile(src, dst)
                print(f"Copied file from {src} to {dst}")
                return filename
        return None
    

    def get_file_from_distant_server(self, new_filename : str) :
        """
            get from distant server
        """
        response = requests.get("http://127.0.0.1:5000/contents/" + new_filename)
        file = response.content

        print(f"HEADERS : {response.headers}")

        if response.headers.get("X-Custom-Filename") == "default.png" :
            self.pretty_print("Main server returned default image, doesn't have the file either")
            save_path = "contents/default.png"
        else : 
            save_path = "contents/" + new_filename
        with open(save_path, "wb") as file_path : 
            file_path.write(file)
        return new_filename


    def update_cache(self, new_file : CachedFile) :
        """
            Method used to update the cache
        """
        self.data.append(new_file)
        if len(self.data) <= self.cache_limit :
            self.pretty_print("Cache length was not reached yet, adding without removal")
            return
        self.pretty_print("Cache length limit reached, removing worst file")
        self.remove_worst_score()
    

    def remove_worst_score(self) :
        """"
            implement worst score removal
        """
        worst_file = self.data[0]
        for file in self.data : 
            if file.last_used < worst_file.last_used : 
                worst_file = file
        print("Removing worst file from cache : ")
        worst_file.file_to_string()
        self.data.remove(worst_file)
        path = "contents/" + worst_file.filename
        os.remove(path)


    def get_next_id(self) -> int : 
        """
            When adding file to data, to setup a unique id
        """
        # ATTENTION CA MARCHE APS EN FAIT OUPS
        return len(self.data) + 1
    
    def pretty_print(self, message) :
        """
            Used to print important messages to follow the course of actions 
        """
        print("\n------------------------------------")
        print(message)
        print("------------------------------------\n")        