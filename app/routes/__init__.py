from sanic import Sanic

from .api.user_routes import api_user_bp
from .web.admin.auth_rout import web_admin_auth_bp
from .web.admin.reg_rout import web_admin_reg_bp
from .web.common.home_rout import web_home_bp


def setup_api(app: Sanic):
    app.blueprint(api_user_bp)

def setup_web(app: Sanic):
    app.blueprint(web_admin_auth_bp)
    app.blueprint(web_home_bp)
    app.blueprint(web_admin_reg_bp)