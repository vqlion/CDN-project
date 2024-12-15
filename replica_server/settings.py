import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
HASH_TABLE_NAME = os.getenv('HASH_TABLE_NAME')
FLASK_DEBUG = os.getenv("FLASK_DEBUG")
PORT = os.getenv('REPLICA_SERVER_PORT')