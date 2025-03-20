from sanic import Blueprint, html
from sqlalchemy.future import select
from .....admin_check import admin_required
from .....config import env
from .....database.connection import get_db
from .....models.db_models import User

web_admin_delete_user_bp = Blueprint("web_admin_delete_user", url_prefix="/web_admin")

@admin_required
async def delete_user(request, admin):
    async with get_db() as session:
        # Если это GET-запрос, просто отображаем форму
        if request.method == "GET":
            result = await session.execute(select(User))
            users = result.scalars().all()

            template = env.get_template("admin/user_crud/delete.html")
            return html(template.render(title="Удаление пользователя", users=users))

        # Если это POST-запрос, обрабатываем удаление
        if request.method == "POST":
            # Получаем данные из формы
            user_id_select = request.form.get("user_id_select")
            user_id_input = request.form.get("user_id_input")

            # Проверяем, что выбран только один способ
            if (user_id_select and user_id_input) or (not user_id_select and not user_id_input):
                result = await session.execute(select(User))
                users = result.scalars().all()
                return html(env.get_template("admin/user_crud/delete.html").render(
                    title="Удаление пользователя",
                    users=users,
                    error="Выберите только один способ: из списка или введите ID вручную!"
                ))

            # Определяем ID пользователя для удаления
            user_id = user_id_select or user_id_input

            try:
                user_id = int(user_id)
            except ValueError:
                result = await session.execute(select(User))
                users = result.scalars().all()
                return html(env.get_template("admin/user_crud/delete.html").render(
                    title="Удаление пользователя",
                    users=users,
                    error="Некорректный ID пользователя!"
                ))

            # Ищем пользователя по ID
            result = await session.execute(select(User).where(User.id == user_id))
            user_to_delete = result.scalars().first()

            if not user_to_delete:
                result = await session.execute(select(User))
                users = result.scalars().all()
                return html(env.get_template("admin/user_crud/delete.html").render(
                    title="Удаление пользователя",
                    users=users,
                    error="Пользователь с таким ID не найден!"
                ))

            # Удаляем пользователя
            await session.delete(user_to_delete)
            await session.commit()

            # Обновляем список пользователей после удаления
            result = await session.execute(select(User))
            users = result.scalars().all()

            return html(env.get_template("admin/user_crud/delete.html").render(
                title="Удаление пользователя",
                users=users,
                success=f"Пользователь {user_to_delete.full_name} успешно удален!"
            ))

# Привязываем маршрут к функции
web_admin_delete_user_bp.add_route(delete_user, "/delete_user", methods=["GET", "POST"])