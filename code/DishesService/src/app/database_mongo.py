from pymongo import MongoClient

import os

# Получаем параметры подключения из переменных окружения
mongo_host = os.environ.get("MONGO_HOST", "localhost")
mongo_port = os.environ.get("MONGO_PORT", "27017")
mongo_user = os.environ.get("MONGO_USER", "admin")
mongo_password = os.environ.get("MONGO_PASSWORD", "password")

# Формируем строку подключения
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"

client = MongoClient(mongo_uri)
db = client["caloriecam"]
images_collection = db["images"]


def save_image_to_mongo(image_data: bytes) -> str:
    """
    Сохраняет изображение в MongoDB.

    :param image_data: Двоичные данные изображения
    :return: Строковое представление ObjectId сохранённого изображения
    """
    image_document = {"data": image_data}
    result = images_collection.insert_one(image_document)
    return str(result.inserted_id)
