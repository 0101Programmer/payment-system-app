# 💻 Асинхронное веб приложение для управленяия платежами, позволяющее работать со следующими сущностями:
- ### Пользователь
- ### Администратор
- ### Счет - имеет баланс, привязан к пользователю
- ### Платеж(пополнение баланса) - хранит уникальный идентификатор и сумму пополнения счета пользователя

# Стек технологий:
- ### База данных - postgresql
- ### sqlalchemy - для работы с базой данных
- ### sanic - веб фреймворк
- ### docker compose
- ### redis
- ### alembic

  # Пользователь имеет следующие возможности:
- Авторизоваться по email/password
- Получить данные о себе(id, email, full_name)
- Получить список своих счетов и балансов
- Получить список своих платежей

# Администратор имеет следующие возможности:
- Авторизоваться по email/password
- Получить данные о себе (id, email, full_name)
- Создать/Удалить/Обновить пользователя
- Получить список пользователей и список его счетов с балансами

# Инструкция для развертывания проекта.

## 1. Создание файла .env в корне проекта (на уровне Dockerfile) со следующими переменными:
> (!) значения подставляются исходя из конфигурации

> Переменные для базы данных (одна ссылка для подключения с помощью Docker, другая — для подключения без него):
- DATABASE_URL (пример: postgresql+asyncpg://user:password@host.docker.internal:5432/db_name)
- NO_DOCKER_DATABASE_URL (пример: postgresql+asyncpg://user:password@localhost:5432/db_name)
  
> конфигурация порта и хоста для Sanic
- SANIC_HOST
- SANIC_PORT

> Admin key (который будет использоваться для возможности регистрации в качестве администратора)
- ADMIN_KEY

> Redis (для управления сессиями), пример конфигурации:
- REDIS_URL=redis://redis:6379/0
- REDIS_PORT=6379
- REDIS_HOST=redis
- NO_DOCKER_REDIS_PORT=6379
- NO_DOCKER_REDIS_HOST=localhost

> Payment secret key (для создания подписи объекта)
- PAYMENT_SECRET_KEY

> Флаг использования Docker (true/false)
- USE_DOCKER=1 (либо 1, либо 0)

## 2. Создание и активация виртуального окружения

> python -m venv .venv

> .venv\Scripts\activate

## 3. Осуществление миграций alembic
> alembic upgrade head

## 4. Запуск проекта (с помощью Docker)
> (!) Перед началом необходимо убедиться, что само приложение Docker Desktop запущено, а также что в файле .env установлено значение 1 для переменной USE_DOCKER

> docker-compose up --build

### Теперь можно перейти на главную страницу приложения — /web_home/.
![Снимок экрана 2025-03-22 132627](https://github.com/user-attachments/assets/665d2467-07d3-4076-a56d-54a9f88fc58f)

#### Здесь есть возможность пройти авторизацию/регистрацию в качестве пользователя или администратора. 
#### Но можно воспользоваться данными, которые были созданы с помощью миграций alembic:
- данные тестового администратора: email: admin@example.com, пароль: 4321
- данные тестового пользователя: email: user@example.com, пароль: 1234

### Авторизировавшись как администратор, попадём на страницу панели управления с данными о текущем администраторе
![Снимок экрана 2025-03-22 133207](https://github.com/user-attachments/assets/d70447cf-33ea-4014-a959-2f4586d4a344)

### Также тут можно выйти из системы или осуществить некоторые действия с пользователями:
- Получить их список
- Создать нового пользователя
- Отредактировать существующего
- Удалить одного из существующих пользователей
  
![Снимок экрана 2025-03-22 133524](https://github.com/user-attachments/assets/78d341f0-a7d5-4fed-b322-e5968c7df82a)


### Переход к списку позволяет посмотреть список счетов пользователя (с возможностью удаления, создания и начисления средств) с балансами

![Снимок экрана 2025-03-22 133836](https://github.com/user-attachments/assets/cd823b2f-7fa3-4ec0-8a11-0ff9d77e90a5)


![Снимок экрана 2025-03-22 134036](https://github.com/user-attachments/assets/65c95f64-7c6b-4f03-9805-e3b8b979f47b)


### Помимо возможности начислить баланс из админпанели, для работы с платежами реализован роут, эмулирующий обработку вебхука от сторонней платежной системы. 
- /api_payment/webhook/payment
  
### Отправим на него запрос со следующими параметрами (через Postman):
```json
{
    "transaction_id": "{{transaction_id}}",
    "user_id": {{user_id}},
    "account_id": {{account_id}},
    "amount": {{amount}},
    "signature": "{{signature}}"
}
```

![Снимок экрана 2025-03-22 134656](https://github.com/user-attachments/assets/50df16cd-a2e8-4ab3-9fc4-299e95fbe81a)

### Где, например:
- transaction_id: 5eae174f-7cd0-472c-bd36-35660f00132b
- user_id: 1
- account_id: 5
- amount: 100

### В pre-request пропишем слудеющий скрипт:
```javascript 
const account_id = pm.variables.get("account_id")
const amount = pm.variables.get("amount")
const transaction_id = pm.variables.get("transaction_id")
const user_id = pm.variables.get("user_id")

const secret_key = "124ааббвв";

const data_string = `${account_id}${amount}${transaction_id}${user_id}${secret_key}`;

const signature = CryptoJS.SHA256(data_string).toString(CryptoJS.enc.Hex);

pm.variables.set("signature", signature);
```

![Снимок экрана 2025-03-22 134929](https://github.com/user-attachments/assets/994a586d-b251-4f28-b31e-23309b0a0d8b)

### В котором secret_key это ключ PAYMENT_SECRET_KEY из файла .env

### Отправим запрос и получим следующий ответ:

![Снимок экрана 2025-03-22 135457](https://github.com/user-attachments/assets/0e1a122a-b8f8-46a5-b86d-87d57a684c47)

### Вернёмся к админ-панели, обновим страницу и увидим, что данные пользователя обновились: появился новый счёт, на который была начислена определённая сумма

![Снимок экрана 2025-03-22 135519](https://github.com/user-attachments/assets/37ae425a-a459-4cc2-b835-33302a48eab5)

### Второй раз отправить запрос с таким же transaction_id не получится

![Снимок экрана 2025-03-22 135705](https://github.com/user-attachments/assets/b0490d03-c889-45de-b3b6-99222f59340f)




