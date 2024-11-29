from LRU_cache import LRUCache
from flask import Flask, send_file, redirect
import os.path

# creates a Flask application 
app = Flask(__name__)
cache = LRUCache()

@app.route("/ask_cache/<filename>") 
def fetch_file(filename) :
    cache.get_file(filename)

    file_path = "contents/" + filename
    default_file_path = "default.png"
    exists = os.path.isfile(file_path)
    if exists :
        return send_file(file_path) 
    return redirect(default_file_path)

# run the application 
if __name__ == "__main__" :
	app.run(host="0.0.0.0", debug=True)