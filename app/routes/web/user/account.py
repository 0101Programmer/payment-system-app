from sanic import Blueprint, html, redirect
from ....config import env
from ....database.connection import get_db
from ....models.db_models import User
from ....redis_utils import get_redis
from ....user_check import user_auth_required

web_user_account_bp = Blueprint("web_user_account", url_prefix="/web_user")

@web_user_account_bp.route("/account", methods=["GET"])
@user_auth_required  # Применяем декоратор для проверки авторизации
async def account(request, user):
    # Отображаем данные пользователя
    template = env.get_template("user/account.html")
    return html(template.render(
        title="Личный кабинет",
        user=user
    ))

@web_user_account_bp.route("/logout", methods=["GET"])
async def logout(request):
    # Получаем session_id из куки
    session_id = request.cookies.get("session_id")
    if session_id:
        # Удаляем данные сессии из Redis
        redis = await get_redis()
        await redis.delete([session_id])

    # Очищаем куки на стороне клиента
    response = redirect("/web_home/")
    response.cookies.add_cookie(
        key="session_id",
        value="",  # Пустое значение
        max_age=0,  # Удаляем куки
        path="/",
        secure=False,  # True, если используется HTTPS
        httponly=True,  # Защита от доступа через JavaScript
        samesite="Lax"  # Защита от CSRF
    )
    return response