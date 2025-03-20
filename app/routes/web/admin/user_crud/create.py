from sanic import Blueprint, text, redirect
from sanic.response import html
from sqlalchemy.future import select

from .....config import env
from .....database.connection import get_db
from .....models.db_models import Admin, User

web_admin_create_user_bp = Blueprint("web_admin_create_user", url_prefix="/web_admin")

@web_admin_create_user_bp.route("/create_user", methods=["GET", "POST"])
async def create_user(request):
    # Проверяем, авторизован ли администратор
    admin_email = request.ctx.session
    if not admin_email:
        return redirect("/web_admin/login")

    async with get_db() as session:
        # Ищем администратора по email
        result = await session.execute(select(Admin).where(Admin.email == admin_email))
        admin = result.scalars().first()

        if not admin:
            return text("Администратор не найден", status=404)

        # Проверяем, является ли пользователь администратором
        if not admin.is_admin:
            return text("Доступ запрещен", status=403)

    # Обработка POST-запроса (сохранение нового пользователя)
    if request.method == "POST":
        # Получаем данные из формы
        email = request.form.get("email")
        password = request.form.get("password")
        full_name = request.form.get("full_name")

        async with get_db() as session:
            # Проверяем, существует ли пользователь с таким email в таблице User
            user_result = await session.execute(select(User).where(User.email == email))
            existing_user = user_result.scalars().first()

            if existing_user:
                # Если пользователь уже существует, рендерим форму с ошибкой
                template = env.get_template("admin/user_crud/create.html")
                return html(template.render(
                    title="Create User",
                    admin=admin,
                    error="Пользователь с таким email уже существует!"
                ))

            # Проверяем, существует ли администратор с таким email в таблице Admin
            admin_result = await session.execute(select(Admin).where(Admin.email == email))
            existing_admin = admin_result.scalars().first()

            if existing_admin:
                # Если администратор уже существует, рендерим форму с ошибкой
                template = env.get_template("admin/user_crud/create.html")
                return html(template.render(
                    title="Create User",
                    admin=admin,
                    error="Email уже используется администратором!"
                ))

            # Создаем нового пользователя
            new_user = User(
                email=email,
                password=password,
                full_name=full_name
            )
            session.add(new_user)
            await session.commit()

            # Передаем сообщение об успехе
            template = env.get_template("admin/user_crud/create.html")
            return html(template.render(
                title="Create User",
                admin=admin,
                success="Пользователь успешно создан!"
            ))

    # Обработка GET-запроса (отображение формы)
    template = env.get_template("admin/user_crud/create.html")
    return html(template.render(title="Create User", admin=admin))