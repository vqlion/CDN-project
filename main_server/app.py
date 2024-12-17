from flask import Flask, send_file, make_response
import os.path
from services.files_service import *
from services.distribution_service import *

from settings import ROOT_DIR, REPLICAS_ADDRESSES_LIST, CONTENTS_FOLDER, FLASK_DEBUG, PORT

# creates a Flask application 
app = Flask(__name__) 

@app.route("/contents/<filename>") 
def fetch_file(filename) : 
    file_path = os.path.join(ROOT_DIR, CONTENTS_FOLDER, filename)
    default_file_path = os.path.join(ROOT_DIR, CONTENTS_FOLDER, "default.png")
    exists = os.path.isfile(file_path)
    if exists :
        return send_file(file_path) 
    default_response = make_response(send_file(default_file_path))
    default_response.headers['X-Custom-Filename'] = "default.png"
    return default_response

# run the application 
if __name__ == "__main__": 
    files_list = list_files(os.path.join(ROOT_DIR, CONTENTS_FOLDER))
    files_hashes = hash_filenames(files_list)
    hash_table = build_hash_table(REPLICAS_ADDRESSES_LIST)

    filename_ips_map = map_filenames_to_ips(files_hashes, hash_table)
    distribute_hash_table(hash_table, REPLICAS_ADDRESSES_LIST)
    distribute_files(filename_ips_map, REPLICAS_ADDRESSES_LIST)

    app.run(host="0.0.0.0", debug=FLASK_DEBUG, port=PORT)