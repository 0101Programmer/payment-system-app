from sanic import Sanic
from .redis_utils import get_redis
from .routes import setup_api, setup_web
from .database.connection import engine
from .models.db_models import Base
from .config import Config

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
            request.ctx.session = session_data
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
            session_id = f"session:{id(request)}"
            response.cookies.add_cookie(
                key="session_id",
                value=session_id,
                max_age=3600,
                path="/",
                secure=False,
                httponly=True,
                samesite="Lax"
            )
        await redis.set(session_id, request.ctx.session, expire=3600)

@app.listener('before_server_start')
async def setup_db(app, loop):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    app.run(host=Config.SANIC_HOST, port=Config.SANIC_PORT)