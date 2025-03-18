from sanic import Blueprint
from sanic.response import html
from ....config import env

# Инициализация Blueprint для админки
web_admin_auth_bp = Blueprint("web_admin", url_prefix="/web_admin")

@web_admin_auth_bp.route("/login", methods=["GET"])
async def login(request):
    # Рендерим шаблон index.html
    template = env.get_template("index.html")
    return html(template.render(title="Login Page"))