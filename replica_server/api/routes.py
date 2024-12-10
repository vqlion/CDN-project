from api.user.file_serving import init as init_user_routes
from api.peer.source_communications import init as init_source_routes

def init(app):
    init_user_routes(app)
    init_source_routes(app)