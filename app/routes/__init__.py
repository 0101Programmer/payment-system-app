from sanic import Sanic

from .api.user_routes import api_user_bp
from .web.admin.admin_panel_rout import web_admin_panel_bp
from .web.admin.auth_rout import web_admin_auth_bp
from .web.admin.reg_rout import web_admin_reg_bp
from .web.admin.user_crud.create import web_admin_create_user_bp
from .web.admin.user_crud.delete import web_admin_delete_user_bp
from .web.admin.user_crud.read import web_admin_get_users_bp
from .web.admin.user_crud.update import web_admin_update_user_bp
from .web.common.home_rout import web_home_bp
from .web.user.account import web_user_account_bp
from .web.user.auth_rout import web_user_auth_bp


def setup_api(app: Sanic):
    app.blueprint(api_user_bp)

def setup_web(app: Sanic):
    # admin
    app.blueprint(web_admin_auth_bp)
    app.blueprint(web_home_bp)
    app.blueprint(web_admin_reg_bp)
    app.blueprint(web_admin_panel_bp)
    app.blueprint(web_admin_create_user_bp)
    app.blueprint(web_admin_get_users_bp)
    app.blueprint(web_admin_delete_user_bp)
    app.blueprint(web_admin_update_user_bp)
    # user
    app.blueprint(web_user_auth_bp)
    app.blueprint(web_user_account_bp)