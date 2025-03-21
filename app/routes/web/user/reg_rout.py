from sanic import Blueprint, redirect
from sanic.response import html
from sqlalchemy.future import select

from ....config import env
from ....database.connection import get_db
from ....models.db_models import User, Admin
from ....redis_utils import get_redis

web_user_reg_bp = Blueprint("web_user_reg", url_prefix="/web_user")

@web_user_reg_bp.route("/register", methods=["GET", "POST"])
async def register(request):
    error = None  # Переменная для хранения сообщений об ошибках

    if request.method == "POST":
        # Получаем данные из формы
        email = request.form.get("email")
        password = request.form.get("password")
        full_name = request.form.get("full_name")

        async with get_db() as session:
            # Проверяем, существует ли пользователь с таким email
            result_user = await session.execute(select(User).where(User.email == email))
            existing_user = result_user.scalars().first()

            # Проверяем, существует ли администратор с таким email
            result_admin = await session.execute(select(Admin).where(Admin.email == email))
            existing_admin = result_admin.scalars().first()

            if existing_user or existing_admin:
                error = "Пользователь или администратор с таким email уже зарегистрирован!"
            else:
                # Создаем нового пользователя
                new_user = User(
                    email=email,
                    password=password,
                    full_name=full_name
                )
                session.add(new_user)
                try:
                    await session.commit()

                    # Создаем сессию для нового пользователя
                    redis = await get_redis()
                    session_id = f"session:{email}"
                    await redis.set(session_id, email, expire=3600)  # Храним сессию 1 час

                    # Устанавливаем session_id в куки
                    response = redirect("/web_user/account")
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
                except Exception as e:
                    await session.rollback()
                    error = f"Ошибка при регистрации: {str(e)}"

    # Если это GET-запрос или есть сообщение об ошибке, отображаем форму
    template = env.get_template("user/reg.html")
    return html(template.render(
        title="Registration Page",
        error=error
    ))