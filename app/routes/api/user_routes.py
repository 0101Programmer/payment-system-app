from sanic import Sanic, json, Blueprint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ...database.connection import get_db
from ...models.user import User

# Создаем Blueprint
api_user_bp = Blueprint("api_user", url_prefix="/api_user")

@api_user_bp.route("/users", methods=["GET"])
async def get_users(request):
    async with get_db() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return json([{"id": user.id, "name": user.name, "email": user.email} for user in users])