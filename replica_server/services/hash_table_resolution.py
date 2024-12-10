import sys
import hashlib
import json

h = hashlib.md5()

def get_ip_from_filename(filename):
    with open('hash-table.json', 'r') as f:
        table = json.load(f)

    h = hashlib.md5()
    h.update(bytes(filename, 'utf-8'))
    filename_hash = h.hexdigest()
    filename_hash = int(filename_hash, 16)

    for entry in table:
        if filename_hash < entry['hash']:
            return entry['ip']
        
# print(get_ip_from_filename('deauzeslt1.png'))