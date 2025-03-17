from sanic import Sanic

from .routes import setup_api
from .database.connection import engine
from .models.user import Base
from .config import Config

app = Sanic("MyApp")

# Настройка API
setup_api(app)

@app.listener('before_server_start')
async def setup_db(app, loop):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    app.run(host=Config.SANIC_HOST, port=Config.SANIC_PORT)