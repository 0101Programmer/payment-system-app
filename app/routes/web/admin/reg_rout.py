from sanic import Blueprint, redirect
from sanic.response import html
from ....config import env, Config
from sqlalchemy.future import select
from ....database.connection import get_db
from ....models.db_models import Admin

web_admin_reg_bp = Blueprint("web_admin_reg", url_prefix="/web_admin")

@web_admin_reg_bp.route("/register", methods=["GET", "POST"])
async def register(request):
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
                    return html("<h1>Администратор с таким email уже зарегистрирован!</h1>")
                else:
                    new_admin = Admin(
                        email=email,
                        password=password,
                        full_name=full_name,
                        is_admin=True
                    )

                    session.add(new_admin)
                    await session.commit()

                    # Сохраняем email администратора в сессию
                    request.ctx.session = email

                    return redirect("/web_admin/admin_panel")
        else:
            return html("<h1>Неверный ключ администратора!</h1>")

    template = env.get_template("admin/reg.html")
    return html(template.render(title="Registration Page"))