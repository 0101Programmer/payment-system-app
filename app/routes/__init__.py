from sanic import Sanic

from .api.user_routes import user_bp

def setup_api(app: Sanic):
    app.blueprint(user_bp)
