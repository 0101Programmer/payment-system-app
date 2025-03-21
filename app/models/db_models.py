from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database.connection import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
    accounts = relationship("Account", back_populates="user")
    payments = relationship("Payment", back_populates="user")

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
    user_id = Column(Integer, ForeignKey("users.id"))
    balance = Column(Float, default=0.0)
    user = relationship("User", back_populates="accounts")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    signature = Column(String)
    user = relationship("User", back_populates="payments")