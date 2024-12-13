from flask import send_from_directory, request, Response
import os.path
from dotenv import load_dotenv
import requests
import re

load_dotenv()

STATIC_FOLDER = os.getenv('FILES_FOLDER')
DEFAULT_FILE_PATH = os.getenv('DEFAULT_FILE_PATH')
CENTRAL_SERVER_ADDRESS = os.getenv('CENTRAL_SERVER_ADDRESS')

def init(app):

    @app.route('/contents/<file>')
    def get_file(file):
        if os.path.isfile(f'./{STATIC_FOLDER}/{file}'):
           return send_from_directory(STATIC_FOLDER, file)
        else: 
            file_data = requests.get(CENTRAL_SERVER_ADDRESS + '/contents/' + file)

            file_path = file_data.url
            file_name = re.match(r'(.*)\/(.*)',file_path).group(2)
            print(file_name)

            with open(f'./{STATIC_FOLDER}/' + file_name, 'wb') as f:
                f.write(file_data.content)

            return send_from_directory(STATIC_FOLDER, file_name)
        