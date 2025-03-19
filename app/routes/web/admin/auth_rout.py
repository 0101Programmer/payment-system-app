from sanic import Blueprint
from sanic.response import html
from ....config import env
from sqlalchemy.future import select
from ....database.connection import get_db
from ....models.db_models import Admin

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
                    return html("<h1>Успешная авторизация!</h1>")
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