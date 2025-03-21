from sanic import Blueprint, html, redirect
from ....config import env
from ....database.connection import get_db
from ....models.db_models import User, Payment
from ....redis_utils import get_redis
from ....user_check import user_auth_required
from sqlalchemy.future import select


web_user_payments_bp = Blueprint("web_user_payments", url_prefix="/web_user")

@web_user_payments_bp.route("/payments", methods=["GET"])
@user_auth_required
async def list_payments(request, user):
    async with get_db() as session:
        result = await session.execute(select(Payment).where(Payment.user_id == user.id))
        payments = result.scalars().all()

    template = env.get_template("user/payments.html")
    return html(template.render(
        title="История платежей",
        payments=payments
    ))