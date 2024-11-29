import sys
import hashlib

h = hashlib.md5()
digest_size_bit = h.digest_size*8
print(digest_size_bit)

table = [
    {
        "hash": (2**digest_size_bit - 1) / 2,
        "ip": "1.1.1.1"
    }, {
        "hash": (2**digest_size_bit - 1),
        "ip": "2.2.2.2"
    }
]

def get_ip_from_filename(filename):
    h.update(bytes(filename, 'utf-8'))
    filename_hash = h.hexdigest()
    filename_hash = int(filename_hash, 16)

    for entry in table:
        if filename_hash < entry['hash']:
            return entry['ip']
        
print(get_ip_from_filename('deault1.png'))