from sanic import Blueprint, html, redirect
from ....config import env
from ....database.connection import get_db
from ....models.db_models import User, Account
from ....redis_utils import get_redis
from ....user_check import user_auth_required
from sqlalchemy.future import select


web_user_pay_accounts_bp = Blueprint("web_user_pay_accounts", url_prefix="/web_user")

@web_user_pay_accounts_bp.route("/pay_accounts", methods=["GET"])
@user_auth_required
async def list_pay_accounts(request, user):
    async with get_db() as session:
        result = await session.execute(select(Account).where(Account.user_id == user.id))
        accounts = result.scalars().all()

    template = env.get_template("user/pay_accounts.html")
    return html(template.render(
        title="Мои счета",
        accounts=accounts
    ))

@web_user_pay_accounts_bp.route("/pay_accounts/create", methods=["POST"])
@user_auth_required
async def create_pay_account(request, user):
    error = None  # Переменная для хранения сообщений об ошибках

    async with get_db() as session:
        new_account = Account(user_id=user.id, balance=0.0)
        session.add(new_account)
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            error = f"Ошибка при создании счёта: {str(e)}"

    # Перенаправляем на страницу "Мои счета" с ошибкой
    async with get_db() as session:
        result = await session.execute(select(Account).where(Account.user_id == user.id))
        accounts = result.scalars().all()

    template = env.get_template("user/pay_accounts.html")
    return html(template.render(
        title="Мои счета",
        accounts=accounts,
        error=error
    ))

@web_user_pay_accounts_bp.route("/pay_accounts/delete/<account_id:int>", methods=["POST"])
@user_auth_required
async def delete_account(request, user, account_id):
    error = None  # Переменная для хранения сообщений об ошибках

    async with get_db() as session:
        # Находим счёт пользователя
        result = await session.execute(select(Account).where(Account.id == account_id, Account.user_id == user.id))
        account = result.scalars().first()

        if not account:
            error = "Счёт не найден"
        else:
            # Удаляем счёт
            await session.delete(account)
            try:
                await session.commit()
            except Exception as e:
                await session.rollback()
                error = f"Ошибка при удалении счёта: {str(e)}"

    # Перенаправляем на страницу "Мои счета" с ошибкой
    async with get_db() as session:
        result = await session.execute(select(Account).where(Account.user_id == user.id))
        accounts = result.scalars().all()

    template = env.get_template("user/pay_accounts.html")
    return html(template.render(
        title="Мои счета",
        accounts=accounts,
        error=error
    ))