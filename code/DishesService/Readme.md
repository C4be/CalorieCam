# DishesService

**DishesService** — это микросервис для работы с блюдами, их калорийностью и предсказаниями на основе изображений. Сервис реализован на Python с использованием FastAPI, SQLAlchemy, PostgreSQL и MongoDB. Предназначен для интеграции в экосистему CalorieCam.

## Основные возможности

- **REST API** для получения информации о блюдах и предсказаниях.
- Загрузка изображений блюд, их сохранение в MongoDB.
- Классификация изображений с помощью нейросети (интеграция через сервис NeuralNetworkService).
- Получение информации о калорийности, белках, жирах и углеводах для каждого блюда.
- Хранение истории предсказаний пользователя.
- Инициализация базы данных блюдами с базовыми характеристиками.

## Архитектура

- **FastAPI** — основной web-фреймворк.
- **SQLAlchemy** — ORM для работы с PostgreSQL.
- **MongoDB** — хранение изображений.
- **Docker** — контейнеризация сервиса.
- **requirements.txt** — список зависимостей.

### Основные директории и файлы

- `src/main.py` — точка входа, настройка FastAPI, CORS, роутинг, инициализация БД.
- `src/app/endpoints.py` — основные API endpoints для загрузки изображений и получения предсказаний.
- `src/app/services.py` — бизнес-логика для работы с блюдами и предсказаниями.
- `src/app/repositories.py` — слой доступа к данным (PostgreSQL).
- `src/app/database_postgres.py` — подключение и работа с PostgreSQL.
- `src/app/database_mongo.py` — подключение и работа с MongoDB.
- `src/app/init_db.py` — инициализация базы данных начальными блюдами.
- `src/requirements.txt` — зависимости Python.
- `src/Dockerfile` — Docker-образ для деплоя сервиса.

## Быстрый старт

1. **Локальный запуск:**
    ```bash
    pip install -r requirements.txt
    uvicorn main:app --reload --host 0.0.0.0 --port 8001
    ```

## Переменные окружения

- Для PostgreSQL:
    - `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- Для MongoDB:
    - `MONGO_HOST`, `MONGO_PORT`, `MONGO_USER`, `MONGO_PASSWORD`

## Примеры API

- `POST /dish/load_image/{prediction_name}` — загрузка изображения и получение предсказания.
- `GET /dish/predict/{predict_id}` — получение информации о предсказании по ID.

## Зависимости

- fastapi
- uvicorn
- pydantic
- python-multipart
- sqlalchemy
- pymongo
- httpx
- psycopg2

## Контейнеризация

В проекте есть Dockerfile для быстрого развертывания сервиса в контейнере. Используется официальный образ Python 3.9-slim, устанавливаются все необходимые зависимости, сервис запускается через Uvicorn.

## Структура базы данных

- **PostgreSQL**: таблицы для хранения информации о блюдах и предсказаниях.
- **MongoDB**: коллекция для хранения изображений.

        