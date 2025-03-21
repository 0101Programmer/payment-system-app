import hashlib

from sqlalchemy.future import select

from .config import Config
from .models.db_models import User, Account, Payment


async def process_payment(session, user_id, account_id, amount, transaction_id):
    # Генерация подписи
    secret_key = Config.PAYMENT_SECRET_KEY
    signature = hashlib.sha256(
        f"{account_id}{amount}{transaction_id}{user_id}{secret_key}".encode()
    ).hexdigest()

    # Проверяем, существует ли транзакция
    result = await session.execute(select(Payment).where(Payment.transaction_id == transaction_id))
    existing_payment = result.scalars().first()

    if existing_payment:
        raise ValueError("Transaction already processed")

    # Ищем пользователя
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise ValueError("User not found")

    # Ищем или создаем счет пользователя
    result = await session.execute(select(Account).where(Account.id == account_id, Account.user_id == user_id))
    account = result.scalars().first()

    if not account:
        account = Account(user_id=user.id, id=account_id, balance=0.0)
        session.add(account)

    # Создаем запись о платеже
    payment = Payment(
        transaction_id=transaction_id,
        account_id=account_id,
        user_id=user_id,
        amount=amount,
        signature=signature
    )
    session.add(payment)

    # Начисляем сумму на счет
    account.balance += amount