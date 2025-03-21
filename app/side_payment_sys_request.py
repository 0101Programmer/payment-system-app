import requests
import hashlib
from config import Config

# Конфигурация
secret_key = Config.PAYMENT_SECRET_KEY
account_id = 1
amount = 100
transaction_id = "5eae174f-7cd0-472c-bd36-35660f00132b"
user_id = 1

# Формирование подписи
data_string = f"{account_id}{amount}{transaction_id}{user_id}{secret_key}"
signature = hashlib.sha256(data_string.encode()).hexdigest()

# URL
url = "http://127.0.0.1:8000/api_payment/webhook/payment"

# Заголовки запроса
headers = {
    "Content-Type": "application/json"
}

# Тело запроса
data = {
    "transaction_id": transaction_id,
    "user_id": user_id,
    "account_id": account_id,
    "amount": amount,
    "signature": signature
}

# Отправка POST-запроса
response = requests.post(url, json=data, headers=headers)

# Вывод ответа от сервера
print("Status Code:", response.status_code)
print("Response Body:", response.json())