from flask import Flask, send_file, redirect, make_response
import os.path
from services.files_service import *
from services.distribution_service import *

ips_list_mock = []

dir_path = '/main_server/contents'

# creates a Flask application 
app = Flask(__name__) 

@app.route("/contents/<filename>") 
def fetch_file(filename) : 
    file_path = os.path.join(dir_path, filename)
    default_file_path = os.path.join(dir_path, "default.png")
    exists = os.path.isfile(file_path)
    if exists :
        return send_file(file_path) 
    default_response = make_response(send_file(default_file_path))
    default_response.headers['X-Custom-Filename'] = "default.png"
    return default_response

# run the application 
if __name__ == "__main__": 
    files_list = list_files(dir_path)
    files_hashes = hash_filenames(files_list)
    hash_table = build_hash_table(ips_list_mock)

    filename_ips_map = map_filenames_to_ips(files_hashes, hash_table)
    distribute_hash_table(hash_table, ips_list_mock)
    distribute_files(filename_ips_map, ips_list_mock)

    app.run(host="0.0.0.0", debug=True)