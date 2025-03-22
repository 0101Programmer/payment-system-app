from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database.connection import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)

    # Связь с аккаунтами (CASCADE: при удалении пользователя удаляются его аккаунты)
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")

    # Связь с платежами (CASCADE: при удалении пользователя удаляются его платежи)
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
    is_admin = Column(Boolean)


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)

    # Внешний ключ на пользователя (CASCADE: при удалении пользователя удаляется его аккаунт)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    balance = Column(Float, default=0.0)

    # Связь с пользователем
    user = relationship("User", back_populates="accounts")

    # Связь с платежами (CASCADE: при удалении аккаунта удаляются связанные платежи)
    payments = relationship("Payment", back_populates="account", cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)

    # Внешний ключ на аккаунт (CASCADE: при удалении аккаунта удаляется платеж)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))

    # Внешний ключ на пользователя (CASCADE: при удалении пользователя удаляется платеж)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    amount = Column(Float)
    signature = Column(String)

    # Связь с пользователем
    user = relationship("User", back_populates="payments")

    # Связь с аккаунтом
    account = relationship("Account", back_populates="payments")