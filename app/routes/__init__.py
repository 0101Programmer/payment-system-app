from sanic import Sanic

from .api.webhook_payment_system_route import api_payment_bp
from .web.admin.admin_panel_rout import web_admin_panel_bp
from .web.admin.auth_rout import web_admin_auth_bp
from .web.admin.payments_edit.edit import web_admin_edit_user_payment_data_bp
from .web.admin.reg_rout import web_admin_reg_bp
from .web.admin.user_crud.create import web_admin_create_user_bp
from .web.admin.user_crud.delete import web_admin_delete_user_bp
from .web.admin.user_crud.read import web_admin_get_users_bp
from .web.admin.user_crud.update import web_admin_update_user_bp
from .web.common.home_rout import web_home_bp
from .web.user.account import web_user_account_bp
from .web.user.auth_rout import web_user_auth_bp
from .web.user.pay_accounts import web_user_pay_accounts_bp
from .web.user.payments import web_user_payments_bp
from .web.user.reg_rout import web_user_reg_bp


def setup_api(app: Sanic):
    app.blueprint(api_payment_bp)

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
    app.blueprint(web_admin_edit_user_payment_data_bp)
    # user
    app.blueprint(web_user_auth_bp)
    app.blueprint(web_user_account_bp)
    app.blueprint(web_user_reg_bp)
    app.blueprint(web_user_pay_accounts_bp)
    app.blueprint(web_user_payments_bp)
