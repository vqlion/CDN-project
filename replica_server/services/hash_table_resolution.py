import hashlib
import json
import os

from settings import ROOT_DIR, HASH_TABLE_NAME

def get_ip_from_filename(filename):
    with open(os.path.join(ROOT_DIR, HASH_TABLE_NAME), 'r') as f:
        table = json.load(f)

    h = hashlib.md5()
    h.update(bytes(filename, 'utf-8'))
    filename_hash = h.hexdigest()
    filename_hash = int(filename_hash, 16)

    for entry in table:
        if filename_hash < entry['hash']:
            return entry['ip']
        
    return None
