import httpx
from fastapi import Depends, UploadFile
from app.repositories import DishRepository, PredictionRepository
from app.database_postgres import get_db
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database_mongo import save_image_to_mongo

class ImageService:
    def __init__(self):
        pass


    async def save_image_to_mongo(self, file: UploadFile):
        """
        Загружает изображение из запроса и сохраняет его в MongoDB
        
        :param file: Загруженный файл изображения
        :return: ID сохраненного изображения в MongoDB
        """
        
        # Чтение содержимого файла
        image_data = await file.read()
        
        # Сохранение в MongoDB и получение ID
        image_id = save_image_to_mongo(image_data)
        
        return image_id


class DishService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = DishRepository(db)


    def get_all_dishes(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all_dishes(skip=skip, limit=limit)


    def get_dish_by_name(self, dish_name: str):
        return self.repo.get_dish_by_name(dish_name=dish_name)


    def get_dish_by_id(self, dish_id: int):
        return self.repo.get_dish_by_id(dish_id=dish_id)


class NeuralNetworkService:
    """Сервис для взаимодействия с внешним API микросервиса NNService"""
    
    def __init__(self):
        # URL сервиса нейросети
        # self.nn_service_url = "http://localhost:8000/nn/predict"
        self.nn_service_url = "http://caloriecam-nn-service:8000/nn/predict"
        
    
    async def classify_image(self, image_id: str) -> str:        
        # Отправляем запрос в сервис нейросети
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.nn_service_url}/{image_id}', timeout=60)
            
            # Проверяем успешность запроса
            response.raise_for_status()
            
            # Получаем результат
            result_data = response.json()
            
            # Возвращаем название класса блюда
            return result_data.get("predicted_class")


class PredictionService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = PredictionRepository(db)
        self.dish_service = DishService(db)


    def get_all_predictions(self, skip: int = 0, limit: int = 5):
        return self.repo.get_all_predictions(skip=skip, limit=limit)


    def get_prediction_by_id(self, prediction_id: int):
        return self.repo.get_prediction_by_id(prediction_id=prediction_id)


    def save_prediction(self, dish_id: int, prediction_name: str, result: str, image_id: str = None):
        return self.repo.create_prediction(
            dish_id=dish_id,
            prediction_name=prediction_name,
            result=result,
            image_id=image_id
        )
