from api.user.file_serving import init as init_user_routes
from api.peer.source_communications import init as init_source_routes
from services.LRU_cache import LRUCache

cache = LRUCache()

def init(app):
    init_user_routes(app, cache)
    init_source_routes(app, cache)
