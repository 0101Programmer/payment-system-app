from sanic import Blueprint, html
from sqlalchemy.future import select
from .....admin_check import admin_required
from .....config import env
from .....database.connection import get_db
from .....models.db_models import User

web_admin_update_user_bp = Blueprint("web_admin_update_user", url_prefix="/web_admin")

@admin_required
async def update_user(request, admin):
    async with get_db() as session:
        # Получаем всех пользователей для выпадающего списка
        result = await session.execute(select(User))
        users = result.scalars().all()

        # Переменная для хранения выбранного пользователя
        user = None
        success = None
        error = None

        if request.method == "POST":
            # Получаем данные из формы
            user_id_select = request.form.get("user_id_select")
            user_id_input = request.form.get("user_id_input")
            user_id = request.form.get("user_id")  # Для сохранения изменений

            # Если форма отправлена для загрузки данных пользователя
            if user_id_select or user_id_input:
                # Проверяем, что выбран только один способ
                if (user_id_select and user_id_input) or (not user_id_select and not user_id_input):
                    error = "Выберите только один способ: из списка или введите ID!"
                else:
                    # Определяем пользователя для редактирования
                    try:
                        user_id_to_find = int(user_id_select or user_id_input)
                        result = await session.execute(select(User).where(User.id == user_id_to_find))
                        user = result.scalars().first()
                    except ValueError:
                        error = "Некорректный ID пользователя!"

                    if not user:
                        error = "Пользователь не найден!"

            # Если форма отправлена для сохранения изменений
            elif user_id:
                # Находим пользователя по ID
                result = await session.execute(select(User).where(User.id == int(user_id)))
                user = result.scalars().first()

                if user:
                    # Получаем новые данные из формы
                    new_email = request.form.get("email")
                    new_full_name = request.form.get("full_name")
                    new_password = request.form.get("password")

                    # Проверяем, что все поля заполнены
                    if not new_email or not new_full_name or not new_password:
                        error = "Все поля обязательны для заполнения!"
                    else:
                        # Обновляем данные пользователя
                        user.email = new_email
                        user.full_name = new_full_name
                        user.password = new_password

                        try:
                            await session.commit()
                            success = "Данные успешно обновлены!"
                        except Exception as e:
                            await session.rollback()
                            error = f"Ошибка при сохранении данных: {str(e)}"
                else:
                    error = "Пользователь не найден!"

        # Рендерим шаблон с данными
        template = env.get_template("admin/user_crud/update.html")
        return html(template.render(
            title="Изменение пользователя",
            users=users,
            user=user,
            success=success,
            error=error
        ))

# Привязываем маршрут к функции
web_admin_update_user_bp.add_route(update_user, "/update_user", methods=["GET", "POST"])