from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List

from app.services import NeuralNetworkService
from app.schemas import GetPrediction

router = APIRouter()


@router.get("/predict/{id}", response_model=GetPrediction)
def get_prediction(
    id: str, nn_service: NeuralNetworkService = Depends()
) -> GetPrediction:
    """
    Возвращает предсказание класса для изображения по его ID из MongoDB.

    :param id: Строковый идентификатор изображения (MongoDB ObjectId)
    :param nn_service: Сервис нейросети (внедряется автоматически через Depends)
    :return: Объект с предсказанным классом
    :raises HTTPException: 404, если изображение не найдено или предсказание не удалось
    """
    prediction: Optional[str] = nn_service.get_prediction(id)
    if prediction:
        return GetPrediction(predicted_class=prediction)

    raise HTTPException(status_code=404, detail="Image not found or prediction failed")


@router.get("/classes", response_model=List[str])
def get_all_classes(nn_service: NeuralNetworkService = Depends()) -> List[str]:
    """
    Возвращает список всех доступных классов.

    :param nn_service: Сервис нейросети
    :return: Список строк – имена классов
    """
    return nn_service.get_all_classes()


@router.get("/classes/count", response_model=int)
def get_classes_count(nn_service: NeuralNetworkService = Depends()) -> int:
    """
    Возвращает количество доступных классов.

    :param nn_service: Сервис нейросети
    :return: Количество классов
    """
    return nn_service.get_cnt_classes()
