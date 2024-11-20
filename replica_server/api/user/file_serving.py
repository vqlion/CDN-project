from flask import send_from_directory
import os.path
from dotenv import load_dotenv

load_dotenv()

STATIC_FOLDER = os.getenv('FILES_FOLDER')
DEFAULT_FILE_PATH = os.getenv('DEFAULT_FILE_PATH')

def init(app):

    @app.route('/files/<file>')
    def get_file(file):
        if os.path.isfile(f'./{STATIC_FOLDER}/{file}'):
           return send_from_directory(STATIC_FOLDER, file)
        else: 
            return send_from_directory(STATIC_FOLDER, DEFAULT_FILE_PATH)