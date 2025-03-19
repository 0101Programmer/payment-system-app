from sanic import Blueprint, redirect
from sanic.response import html
from ....config import env, Config
from sqlalchemy.future import select
from ....database.connection import get_db
from ....models.db_models import Admin
from ....redis_utils import get_redis  # Импортируем функцию для работы с Redis

# Инициализация Blueprint для админки
web_admin_auth_bp = Blueprint("web_admin_auth", url_prefix="/web_admin")

@web_admin_auth_bp.route("/login", methods=["GET", "POST"])
async def login(request):
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
                        secure=False,  # Установите True, если используете HTTPS
                        httponly=True,  # Защита от доступа через JavaScript
                        samesite="Lax"  # Защита от CSRF
                    )
                    return response
                else:
                    return html("<h1>Некорректный пароль!</h1>")
            else:
                # Если администратор не найден, предлагаем зарегистрироваться
                return html("""
                <h1>Администратор с указанным email не найден!</h1>
                <p><a href="/web_admin/register">Перейти к регистрации</a></p>
                """)

    # Если это GET-запрос, отображаем форму
    template = env.get_template("admin/auth.html")
    return html(template.render(title="Login Page"))