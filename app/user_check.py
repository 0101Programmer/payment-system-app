from functools import wraps

from sanic import text, redirect
from sqlalchemy.future import select

from .database.connection import get_db
from .models.db_models import User
from .redis_utils import get_redis


def user_auth_required(func):
    """
    Декоратор для проверки авторизованной сессии пользователя.
    Перенаправляет на страницу входа, если пользователь не авторизован.
    """
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        # Получаем session_id из кук
        session_id = request.cookies.get("session_id")
        if not session_id:
            return redirect("/web_user/login")  # Перенаправляем на страницу входа

        # Проверяем сессию в Redis
        redis = await get_redis()
        email = await redis.get(session_id)

        if not email:
            return redirect("/web_user/login")  # Сессия недействительна

        # Ищем пользователя по email в базе данных
        async with get_db() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalars().first()

            if not user:
                return text("Пользователь не найден", status=404)

        # Если все проверки пройдены, передаем пользователя в оригинальную функцию
        return await func(request, user=user, *args, **kwargs)

    return wrapper