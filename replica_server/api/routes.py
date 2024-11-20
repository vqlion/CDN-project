from api.user.file_serving import init as init_user_routes

def init(app):
    init_user_routes(app)