from flask import Flask
from api.routes import init as init_routes

from settings import FLASK_DEBUG, PORT

def create_app():
    app = Flask(__name__)
    init_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=FLASK_DEBUG, port=PORT)