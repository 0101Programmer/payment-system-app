import hashlib

from sanic import Blueprint, json

from ...config import Config
from ...database.connection import get_db
from ...process_payment_func import process_payment

api_payment_bp = Blueprint("api_payment", url_prefix="/api_payment")

@api_payment_bp.route("/webhook/payment", methods=["POST"])
async def process_webhook(request):
    data = request.json
    transaction_id = data.get("transaction_id")
    account_id = data.get("account_id")
    user_id = data.get("user_id")
    amount = data.get("amount")
    signature = data.get("signature")

    # Проверяем, что все обязательные поля присутствуют
    if not all([transaction_id, account_id, user_id, amount, signature]):
        return json({"error": "Invalid data"}, status=400)

    # Проверяем подпись
    secret_key = Config.PAYMENT_SECRET_KEY
    expected_signature = hashlib.sha256(
        f"{account_id}{amount}{transaction_id}{user_id}{secret_key}".encode()
    ).hexdigest()

    if signature != expected_signature:
        return json({"error": "Invalid signature"}, status=400)

    async with get_db() as session:
        try:
            await process_payment(session, user_id, account_id, amount, transaction_id)
            await session.commit()
        except ValueError as e:
            await session.rollback()
            return json({"error": str(e)}, status=400)
        except Exception as e:
            await session.rollback()
            return json({"error": f"Database error: {str(e)}"}, status=500)

    return json({"message": "Payment processed successfully"}, status=200)