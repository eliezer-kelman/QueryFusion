from flask import Flask

from app.routes.html_routes import index_blueprint
from app.routes.queries_routes import query_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(index_blueprint, url_prefix='/')
    app.register_blueprint(query_blueprint, url_prefix='/api')
    return app
