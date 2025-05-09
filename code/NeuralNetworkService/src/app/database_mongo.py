from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Optional

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


def get_image_from_mongo(image_id: str) -> Optional[bytes]:
    """
    Получает бинарные данные изображения из MongoDB по его ObjectId.

    :param image_id: Строковый ObjectId изображения (из MongoDB)
    :return: Бинарные данные изображения или None, если не найдено
    """
    try:
        obj_id = ObjectId(image_id)
    except Exception:
        return None

    image = images_collection.find_one({"_id": obj_id})
    if image and "data" in image:
        return image["data"]
    return None
