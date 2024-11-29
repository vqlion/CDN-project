from flask import Flask, send_file
import os.path

# creates a Flask application 
app = Flask(__name__) 

@app.route("/<filename>") 
def fetch_file(filename) : 
    file_path = "contents/" + filename
    default_file_path = "contents/default.png"
    exists = os.path.isfile(file_path)
    if exists :
        return send_file(file_path) 
    return send_file(default_file_path) 

# run the application 
if __name__ == "__main__": 
	app.run(host="0.0.0.0", debug=True)