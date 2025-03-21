from sanic import Blueprint, redirect
from sanic.response import html
from ....config import env, Config
from sqlalchemy.future import select
from ....database.connection import get_db
from ....models.db_models import Admin
from ....redis_utils import get_redis

web_admin_reg_bp = Blueprint("web_admin_reg", url_prefix="/web_admin")

@web_admin_reg_bp.route("/register", methods=["GET", "POST"])
async def register(request):
    error = None  # Переменная для хранения сообщений об ошибках

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        full_name = request.form.get("full_name")
        admin_key = request.form.get("admin_key")

        if admin_key == Config.ADMIN_KEY:
            async with get_db() as session:
                result = await session.execute(select(Admin).where(Admin.email == email))
                existing_admin = result.scalars().first()

                if existing_admin:
                    error = "Администратор с таким email уже зарегистрирован!"
                else:
                    new_admin = Admin(
                        email=email,
                        password=password,
                        full_name=full_name,
                        is_admin=True
                    )

                    session.add(new_admin)
                    try:
                        await session.commit()

                        # Создаем уникальный session_id для администратора
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
                    except Exception as e:
                        await session.rollback()
                        error = f"Ошибка при регистрации: {str(e)}"
        else:
            error = "Неверный ключ администратора!"

    # Если это GET-запрос или есть ошибка, отображаем форму
    template = env.get_template("admin/reg.html")
    return html(template.render(title="Registration Page", error=error))