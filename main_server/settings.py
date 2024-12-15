import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

PORT = os.getenv('MAIN_SERVER_PORT')
REPLICAS_ADDRESSES_LIST = os.getenv("REPLICAS_ADDRESSES").split(',')
print(REPLICAS_ADDRESSES_LIST)
CONTENTS_FOLDER = os.getenv('MAIN_SERVER_CONTENT_FOLDER')
FLASK_DEBUG = os.getenv('FLASK_DEBUG')