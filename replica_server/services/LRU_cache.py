from typing import Dict, List
from services.cached_file import CachedFile, Origin
from services.hash_table_resolution import get_ip_from_filename
from time import time, sleep
import requests
from datetime import datetime
from os import walk
import os 
from PIL import Image
import shutil

from settings import ROOT_DIR

"""
    TO-DO : 

    - Pb quand on demande deux fois une default image, y'en a quand meme une qui est supprimée du côté du replica
    - Différencier static et contents pour les fichiers de cache et ceux de base 
    - ajouter un .env

    - add logging ? 
    - add error handling ? 
    - get current files via a json instead of data dict ? 
    - replace user and server interactions with api calls
    - pb de default.png dans main_server (see readme)
    - pb de taille de cache (n-1 ?)

""" 

class LRUCache() : 
    def __init__(self):
        print("CREATING AND INITIALIZING THE CACHE")
        self.data : List(CachedFile) = [] # list de CachedFiles
        self.cache_limit : int = 5 # num of files that can be hold in the cache
        self.empty_all_content_directories() # AVANT TOUT : vider le static et le cache


    def empty_all_content_directories(self) : 
        print("Emptying all cache directories for path : ")
        base_path = '/home/eolia/Documents/INSA/5TC/CDN/CDN-project/replica_server'
        paths = ["contents", "static"]
        for path in paths:
            full_path = os.path.join(base_path, path)
            print(full_path)
            if os.path.exists(full_path):  # Vérifie si le répertoire existe
                shutil.rmtree(full_path)  # Supprime le répertoire entier
                os.mkdir(full_path)  # Le recrée vide
            else:
                os.mkdir(full_path)  # Crée le répertoire s'il n'existe pas


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
        print("\n\n Filling data with the files retreived from the main server at init : ")
        paths = ["contents", "static"] # no need to add static as it is emptied at initialisation
        for path in paths : 
            full_path = os.path.join(ROOT_DIR, path)
            filenames = next(walk(full_path), (None, None, []))[2]  # [] if no file
            for id, filename in enumerate(filenames) : 
                origin = Origin.CACHED if path == "contents" else Origin.STATIC
                new_file = CachedFile(filename=filename, id=id, origin=origin)
                self.data.append(new_file)
        self.pretty_print("Cache state at init :")
        self.cache_to_string()
    

    def cache_to_string(self) : 
        """
            To string method to print whole content of the cache
        """
        for file in self.data : 
            file.file_to_string()


    def get_file(self, filename) -> CachedFile:
        """
            If file is already in the cache call send_directly
            Else call send_and_change_cache
        """
        self.pretty_print(f"Got asked for file : {filename}")
        file = self.retreive_file_from_dataset(filename=filename)
        if file is not None :
            self.pretty_print("This file is present in my cache")
            sent_file = self.send_directly(file)
        else : 
            self.pretty_print("Don't have the file, need to fetch it")
            sent_file = self.send_and_change_cache(filename)
        return sent_file


    def send_file(self, file : CachedFile) -> CachedFile :
        """
            send file back to the user that asked
        """
        self.pretty_print(f"SENDING FILE :")
        file.file_to_string()
        return file


    def send_directly(self, file : CachedFile) -> CachedFile:
        """
            send the asked file and update its timestamp 
        """
        file.change_last_used()
        return self.send_file(file)


    def send_and_change_cache(self, filename : str) -> CachedFile :
        """
            get the asked file from distant server, send it and update the local cache
        """
        new_file = self.get_file_from_distant_server(filename)
        if new_file is None : 
            print("File retreival was impossible, no one has it. Sorry owo")
        new_file = CachedFile(new_file, self.get_next_id(), origin=Origin.CACHED)
        self.update_cache(new_file)
        return self.send_file(new_file)


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

        request_ip = get_ip_from_filename(new_filename)

        if request_ip == None:
            return None

        response = requests.get(request_ip + "/ask_cache/" + new_filename)
        file = response.content

        print(f"HEADERS : {response.headers}")

        if response.headers.get("X-Custom-Filename") == "default.png" :
            self.pretty_print("Main server returned default image, doesn't have the file either")
            new_filename = os.path.join(ROOT_DIR, "default.png")
        save_path = os.path.join(ROOT_DIR, "contents/", new_filename)
        with open(save_path, "wb") as file_path : 
            file_path.write(file)
        return new_filename


    def update_cache(self, new_file : CachedFile) :
        """
            Method used to update the cache
        """
        self.data.append(new_file)
        if self.compute_cache_current_size() <= self.cache_limit :
            self.pretty_print("Cache length was not reached yet, adding without removal")
            return
        self.pretty_print("Cache length limit reached, removing worst file")
        self.remove_worst_score()

    def compute_cache_current_size(self) : 
        size = 0
        for file in self.data : 
            if file.origin == Origin.CACHED : 
                size+=1
        return size
    

    def remove_worst_score(self) :
        """"
            implement worst score removal
        """
        worst_file = next((first_file for first_file in self.data if first_file.origin == Origin.CACHED), None) # find the first file of the list with STATIC origin
        for file in self.data : 
            if file.origin == Origin.CACHED : 
                if file.last_used < worst_file.last_used : 
                    worst_file = file
        print("Removing worst file from cache : ")
        worst_file.file_to_string()
        self.data.remove(worst_file)
        path = "replica_server/contents/" + worst_file.filename
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