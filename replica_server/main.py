from services.LRU_cache import LRUCache
from flask import Flask, send_file, redirect, request, make_response
import os.path

# creates a Flask application 
app = Flask(__name__)
cache = LRUCache()

@app.route("/hello") 
def hello(): 
    return "Hello, Welcome to GeeksForGeeks"
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

# run the application 
if __name__ == "__main__" :
	app.run(host="0.0.0.0", port=5001, debug=True)