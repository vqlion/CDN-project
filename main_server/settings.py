import os
import config as cfg

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
print(ROOT_DIR)

PORT = cfg.MAIN_SERVER_PORT
REPLICAS_ADDRESSES_LIST = cfg.REPLICAS_ADDRESSES.split(',')
print(REPLICAS_ADDRESSES_LIST)
CONTENTS_FOLDER = cfg.MAIN_SERVER_CONTENT_FOLDER
FLASK_DEBUG = cfg.FLASK_DEBUG