from fastapi import Depends
from typing import List, Optional
from tempfile import NamedTemporaryFile
import os

from app.neural_network import NeuralNetwork
from app.database_mongo import get_image_from_mongo


class NeuralNetworkService:
    """
    Сервис для обработки изображений и получения предсказаний от нейросети.
    """

    def __init__(self, engine: NeuralNetwork = Depends()) -> None:
        """
        Инициализирует сервис с экземпляром нейросети.

        :param engine: Зависимость, экземпляр класса NeuralNetwork
        """
        self.NNEngine: NeuralNetwork = engine

    def get_prediction(self, image_id: str) -> Optional[str]:
        """
        Получает предсказание от нейросети по ID изображения из MongoDB.

        :param image_id: Строковый ID изображения (ObjectId в MongoDB)
        :return: Название предсказанного класса или None, если не удалось
        """
        image_data: Optional[bytes] = get_image_from_mongo(image_id=image_id)

        if not image_data:
            return None

        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(image_data)
            temp_file_path = temp_file.name

        try:
            idx: int = self.NNEngine.get_prediction(temp_file_path)
            class_name: str = self.NNEngine.class_names[idx]
        finally:
            os.remove(temp_file_path)

        return class_name

    def get_all_classes(self) -> List[str]:
        """
        Возвращает список всех доступных классов.

        :return: Список строк
        """
        return self.NNEngine.class_names

    def get_cnt_classes(self) -> int:
        """
        Возвращает количество классов.

        :return: Целое число
        """
        return self.NNEngine.conf.NUM_CLASSES
