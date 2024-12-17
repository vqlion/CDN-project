from flask import send_from_directory, request, Response
import os.path
from dotenv import load_dotenv
import requests
import re
import json

load_dotenv()

STATIC_FOLDER = os.getenv('FILES_FOLDER')
DEFAULT_FILE_PATH = os.getenv('DEFAULT_FILE_PATH')
CENTRAL_SERVER_ADDRESS = os.getenv('CENTRAL_SERVER_ADDRESS')

def init(app, cache):

    @app.route('/upload', methods=["PUT"])
    def upload_files():
        if request.files:
            files_list = request.files.values()
            for file in files_list:
                file.save(os.path.join('./replica_server/static', file.filename))
                print(f"Just saved the file : {file.filename} in static dir")
            
            cache.fill_data_with_existing_files()
            return Response("", 200)
        return Response("", 500)
        
    @app.route('/upload-hash-table', methods=["PUT"])
    def upload_hash_table():
        if request.json:
            with open("hash-table.json", "w") as json_file:
                json.dump(request.json["hash_table"], json_file)
            return Response("", 200)
        return Response("", 500)