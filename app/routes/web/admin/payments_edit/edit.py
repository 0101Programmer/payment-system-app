from sanic import Blueprint, html, redirect
from sqlalchemy.future import select

from .....admin_check import admin_required
from .....config import env
from .....database.connection import get_db
from .....models.db_models import User, Account, Payment

web_admin_edit_user_payment_data_bp = Blueprint("web_admin_edit_user_payment_data", url_prefix="/web_admin")

@web_admin_edit_user_payment_data_bp.route("/user/<user_id:int>/create_account", methods=["POST"])
@admin_required
async def create_account(request, admin, user_id):
    async with get_db() as session:
        # Ищем пользователя по ID
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if not user:
            return html("<h1>Пользователь не найден</h1>", status=404)

        # Создаем новый счет
        new_account = Account(user_id=user.id, balance=0.0)
        session.add(new_account)
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            return html(f"<h1>Ошибка при создании счёта: {str(e)}</h1>", status=500)

    # Перенаправляем обратно на страницу данных пользователя
    return redirect(f"/web_admin/user/{user_id}/payment_data")

@web_admin_edit_user_payment_data_bp.route("/user/<user_id:int>/delete_account/<account_id:int>", methods=["POST"])
@admin_required
async def delete_account(request, admin, user_id, account_id):
    async with get_db() as session:
        # Ищем пользователя по ID
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if not user:
            return html("<h1>Пользователь не найден</h1>", status=404)

        # Ищем счет пользователя
        result = await session.execute(select(Account).where(Account.id == account_id, Account.user_id == user_id))
        account = result.scalars().first()

        if not account:
            return html("<h1>Счёт не найден</h1>", status=404)

        # Удаляем счет
        await session.delete(account)
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            return html(f"<h1>Ошибка при удалении счёта: {str(e)}</h1>", status=500)

    # Перенаправляем обратно на страницу данных пользователя
    return redirect(f"/web_admin/user/{user_id}/payment_data")


@web_admin_edit_user_payment_data_bp.route("/user/<user_id:int>/add_amount/<account_id:int>", methods=["POST"])
@admin_required
async def add_amount(request, admin, user_id, account_id):
    # Получаем сумму из формы
    try:
        amount = float(request.form.get("amount"))
    except (ValueError, TypeError):
        return html("<h1>Ошибка: Некорректная сумма</h1>", status=400)

    async with get_db() as session:
        # Ищем пользователя по ID
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if not user:
            return html("<h1>Пользователь не найден</h1>", status=404)

        # Ищем счет пользователя
        result = await session.execute(select(Account).where(Account.id == account_id, Account.user_id == user_id))
        account = result.scalars().first()

        if not account:
            return html("<h1>Счёт не найден</h1>", status=404)

        # Увеличиваем баланс счета
        account.balance += amount
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            return html(f"<h1>Ошибка при начислении суммы: {str(e)}</h1>", status=500)

    # Перенаправляем обратно на страницу данных пользователя
    return redirect(f"/web_admin/user/{user_id}/payment_data")
