from sanic import Blueprint, text, redirect
from sanic.response import html
from ....config import env, Config
from sqlalchemy.future import select
from ....database.connection import get_db
from ....models.db_models import Admin
from ....redis_utils import get_redis

web_admin_panel_bp = Blueprint("web_admin_panel", url_prefix="/web_admin")

@web_admin_panel_bp.route("/admin_panel", methods=["GET"])
async def admin_panel(request):
    # Получаем email администратора из сессии
    admin_email = request.ctx.session  # Email уже загружен в middleware

    if not admin_email:
        return redirect("/web_admin/login")

    async with get_db() as session:
        # Ищем администратора по email
        result = await session.execute(select(Admin).where(Admin.email == admin_email))
        admin = result.scalars().first()

        if not admin:
            return text("Администратор не найден", status=404)

    # Рендерим шаблон личного кабинета
    template = env.get_template("admin/admin_panel.html")
    return html(template.render(title="Admin Panel", admin=admin))

@web_admin_panel_bp.route("/logout", methods=["GET"])
async def logout(request):
    # Получаем session_id из куки
    session_id = request.cookies.get("session_id")
    if session_id:
        # Удаляем данные сессии из Redis
        redis = await get_redis()
        await redis.delete([session_id])

    # Очищаем куки на стороне клиента
    response = redirect("/web_home/")
    response.cookies.add_cookie(
        key="session_id",
        value="",  # Пустое значение
        max_age=0,  # Удаляем куки
        path="/",
        secure=False,
        httponly=True,
        samesite="Lax"
    )
    return response