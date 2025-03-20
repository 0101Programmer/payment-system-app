from functools import wraps

from sanic import text, redirect
from sqlalchemy.future import select

from .database.connection import get_db
from .models.db_models import Admin


def admin_required(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
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

        # Если все проверки пройдены, вызываем оригинальную функцию
        return await func(request, admin=admin, *args, **kwargs)

    return wrapper