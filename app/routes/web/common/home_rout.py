from sanic import Blueprint
from sanic.response import html
from ....config import env

web_home_bp = Blueprint("web_home", url_prefix="/web_home")

@web_home_bp.route("/", methods=["GET"])
async def home(request):
    template = env.get_template("index.html")
    return html(template.render(title="Home Page"))