from flask import send_from_directory, request, Response
import os.path
import requests
import re
import json

from settings import ROOT_DIR, HASH_TABLE_NAME

def init(app, cache):

    @app.route('/upload', methods=["PUT"])
    def upload_files():
        if request.files:
            files_list = request.files.values()
            for file in files_list:
                file.save(os.path.join(ROOT_DIR, 'static', file.filename))
                print(f"Just saved the file : {file.filename} in static dir")
            
            cache.fill_data_with_existing_files()
            return Response("", 200)
        return Response("", 500)
        
    @app.route('/upload-hash-table', methods=["PUT"])
    def upload_hash_table():
        print(os.path.join(ROOT_DIR, HASH_TABLE_NAME))
        if request.json:
            with open(os.path.join(ROOT_DIR, HASH_TABLE_NAME), "w") as json_file:
                json.dump(request.json["hash_table"], json_file)
            return Response("", 200)
        return Response("", 500)