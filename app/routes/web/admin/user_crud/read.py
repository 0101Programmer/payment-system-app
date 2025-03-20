from sanic import Blueprint, html

from .....admin_check import admin_required
from .....config import env
from sqlalchemy.future import select
from .....database.connection import get_db
from .....models.db_models import Admin, User

web_admin_get_users_bp = Blueprint("web_admin_get_users", url_prefix="/web_admin")

@admin_required
async def get_all_users(request, admin):
    # Получаем всех пользователей
    async with get_db() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

    # Рендерим шаблон с таблицей пользователей
    template = env.get_template("admin/user_crud/get_all_users.html")
    return html(template.render(title="Get All Users", admin=admin, users=users))

# Привязываем маршрут к функции
web_admin_get_users_bp.add_route(get_all_users, "/get_all_users", methods=["GET"])