FLASK_ENV='development'
FLASK_DEBUG=1

HASH_TABLE_NAME='hash-table.json'

MAIN_SERVER_ADDRESS='http://167.8.10.2:5000' # including the port, make sure it matches the one below
MAIN_SERVER_PORT=5000
MAIN_SERVER_CONTENT_FOLDER='contents'

REPLICA_SERVER_PORT=5001

REPLICAS_ADDRESSES="http://167.8.6.10:5001,http://167.8.6.11:5001" # format is "ip1,ip2,..." without spaces