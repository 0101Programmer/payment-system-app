from sanic import Sanic
from .redis_utils import get_redis
from .routes import setup_api, setup_web
from .database.connection import engine
from .models.db_models import Base
from .config import Config
import uuid  # Для генерации уникальных session_id

app = Sanic("MyApp")

# Настройка API
setup_api(app)

# Настройка веб-интерфейса
setup_web(app)

@app.middleware("request")
async def load_session(request):
    # Получаем session_id из куки
    session_id = request.cookies.get("session_id")
    if session_id:
        redis = await get_redis()
        session_data = await redis.get(session_id)
        if session_data:
            request.ctx.session = session_data  # Убираем .decode()
        else:
            request.ctx.session = None
    else:
        request.ctx.session = None

@app.middleware("response")
async def save_session(request, response):
    # Сохраняем данные сессии в Redis
    if hasattr(request.ctx, "session") and request.ctx.session:
        redis = await get_redis()
        session_id = request.cookies.get("session_id")
        if not session_id:
            session_id = f"session:{uuid.uuid4()}"  # Генерируем уникальный session_id
            response.cookies.add_cookie(
                key="session_id",
                value=session_id,
                max_age=3600,  # Куки действительны 1 час
                path="/",
                secure=False,  # True, если используется HTTPS
                httponly=True,  # Защита от доступа через JavaScript
                samesite="Lax"  # Защита от CSRF
            )
        await redis.set(session_id, request.ctx.session, expire=3600)  # Храним сессию 1 час

@app.listener('before_server_start')
async def setup_db(app, loop):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    app.run(host=Config.SANIC_HOST, port=Config.SANIC_PORT)