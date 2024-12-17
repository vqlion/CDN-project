from os import listdir
from os.path import isfile, join
import hashlib

h = hashlib.md5()
digest_size_bit = h.digest_size*8
ips_list_mock = []

dir_path = '/CDN-project/main_server/contents'

def list_files(path):
    files_list = [f for f in listdir(path) if isfile(join(path, f))]
    return files_list

def hash_filenames(files_list):
    list_hashes = []
    for filename in files_list:
        h = hashlib.md5()
        h.update(bytes(filename, 'utf-8'))
        filename_hash = int(h.hexdigest(), 16)

        list_hashes.append({ "filename": filename, "hash": filename_hash })

    return list_hashes

def build_hash_table(ip_list):
    hash_table = []

    for i, ip in enumerate(ip_list):
        hash_table.append({
            "hash": int((2**digest_size_bit - 1) * ((i + 1) / len(ip_list))),
            "ip": ip
        })

    return hash_table

def map_filenames_to_ips(hash_filenames, hash_table):
    filename_ips = []
    for filename_hash in hash_filenames:
        for entry in hash_table:
            if filename_hash["hash"] < entry["hash"]:
                filename_ips.append({
                    "filename": filename_hash["filename"],
                    "ip": entry["ip"]
                })
                break
    return filename_ips

# files_list = list_files(dir_path)
# files_hashes = hash_filenames(files_list)

# hash_table = build_hash_table(ips_list_mock)
# print(files_hashes)
# print(hash_table)
# print(map_filenames_to_ips(files_hashes, hash_table))