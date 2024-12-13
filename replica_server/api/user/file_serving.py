from services.LRU_cache import LRUCache
from flask import Flask, send_file, redirect, request, make_response
import os.path

cache = LRUCache()

def init(app):

    @app.route("/ask_cache/<filename>") 
    def fetch_file(filename) :
        src_addr = request.remote_addr
        print(f"REMOTE ADDRESSSSSS : {src_addr}")
        cache.get_file(filename)

        file_path = "contents/" + filename
        default_file_path = "contents/default.png"
        exists = os.path.isfile(file_path)
        if exists :
            return send_file(file_path) 
        default_response = make_response(send_file(default_file_path))
        default_response.headers['X-Custom-Filename'] = "default.png"
        return default_response