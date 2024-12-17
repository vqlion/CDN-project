import requests

ips_list_mock = []

dir_path = '/main_server/contents'


def distribute_files(filename_ips, ips_list):
    for ip in ips_list:
        filenames = [e['filename'] for e in filename_ips if e['ip'] == ip]
        files_send = {}
        for filename in filenames:
            files_send[filename] = open(f'./main_server/contents/{filename}', 'rb')
        print(files_send)
        print(ip)
        requests.put(ip + "/upload", files=files_send)

def distribute_hash_table(hash_table, ips_list):
    for ip in ips_list:
        requests.put(ip + "/upload-hash-table", json={'hash_table': hash_table})
    
