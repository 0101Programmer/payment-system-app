from sanic import Blueprint, redirect
from sanic.response import html
from sqlalchemy.future import select

from ....config import env
from ....database.connection import get_db
from ....models.db_models import Admin
from ....redis_utils import get_redis

# Инициализация Blueprint для админки
web_admin_auth_bp = Blueprint("web_admin_auth", url_prefix="/web_admin")

@web_admin_auth_bp.route("/login", methods=["GET", "POST"])
async def login(request):
    error = None  # Переменная для хранения сообщений об ошибках

    if request.method == "POST":
        # Получаем данные из формы
        email = request.form.get("email")
        password = request.form.get("password")

        async with get_db() as session:
            # Ищем администратора по email
            result = await session.execute(select(Admin).where(Admin.email == email))
            admin = result.scalars().first()

            if admin:
                # Если администратор найден, проверяем пароль
                if admin.password == password:
                    # Создаем уникальный session_id
                    redis = await get_redis()
                    session_id = f"session:{email}"
                    await redis.set(session_id, email, expire=3600)  # Храним сессию 1 час

                    # Устанавливаем session_id в куки
                    response = redirect("/web_admin/admin_panel")
                    response.cookies.add_cookie(
                        key="session_id",
                        value=session_id,
                        max_age=3600,  # Куки действительны 1 час
                        path="/",
                        secure=False,  # True, если используется HTTPS
                        httponly=True,  # Защита от доступа через JavaScript
                        samesite="Lax"  # Защита от CSRF
                    )
                    return response
                else:
                    error = "Некорректный пароль!"
            else:
                error = "Администратор с указанным email не найден!"

    # Если это GET-запрос или есть ошибка, отображаем форму
    template = env.get_template("admin/auth.html")
    return html(template.render(title="Login Page", error=error))