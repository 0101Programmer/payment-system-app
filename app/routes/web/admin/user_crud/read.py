from sanic import Blueprint, html
from sqlalchemy.future import select

from .....admin_check import admin_required
from .....config import env
from .....database.connection import get_db
from .....models.db_models import User, Account, Payment

web_admin_get_users_bp = Blueprint("web_admin_get_users", url_prefix="/web_admin")

@web_admin_get_users_bp.route("/get_all_users", methods=["GET"])
@admin_required
async def get_all_users(request, admin):
    # Получаем всех пользователей
    async with get_db() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

    # Рендерим шаблон с таблицей пользователей
    template = env.get_template("admin/user_crud/get_all_users.html")
    return html(template.render(title="Get All Users", admin=admin, users=users))


@web_admin_get_users_bp.route("/user/<user_id:int>/payment_data", methods=["GET"])
@admin_required
async def get_user_payment_data(request, admin, user_id):
    # Получаем данные пользователя, его счетов и платежей
    async with get_db() as session:
        # Ищем пользователя по ID
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if not user:
            return html("<h1>Пользователь не найден</h1>", status=404)

        # Ищем счета пользователя
        result = await session.execute(select(Account).where(Account.user_id == user_id))
        accounts = result.scalars().all()

        # Ищем платежи пользователя
        result = await session.execute(select(Payment).where(Payment.user_id == user_id))
        payments = result.scalars().all()

    # Рендерим шаблон с данными о пользователе, его счетах и платежах
    template = env.get_template("admin/user_crud/get_user_data.html")
    return html(template.render(
        title=f"Данные пользователя {user.full_name}",
        user=user,
        accounts=accounts,
        payments=payments
    ))