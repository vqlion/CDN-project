from flask import Flask, send_file, redirect, request, make_response
from services.cached_file import Origin
import os.path

def init(app, cache):

    @app.route("/ask_cache/<filename>") 
    def fetch_file(filename) :
        src_addr = request.remote_addr
        print(f"REMOTE ADDRESSSSSS : {src_addr}")
        file_to_send = cache.get_file(filename)

        file_dir = "contents" if file_to_send.origin == Origin.CACHED else "static"
        file_name = file_to_send.filename
        file_path = os.path.join(file_dir, file_name)
        print(f"FILE PATH IS {file_path}")
        default_file_path = "contents/default.png"
        exists = os.path.isfile(file_path)
        return send_file(file_path) 
        if exists :
            return send_file(file_path) 
        default_response = make_response(send_file(default_file_path))
        default_response.headers['X-Custom-Filename'] = "default.png"
        return default_response