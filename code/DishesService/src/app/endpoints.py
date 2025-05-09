from fastapi import APIRouter, UploadFile, File, Depends
from app.services import (
    ImageService,
    PredictionService,
    DishService,
    NeuralNetworkService,
)
from app.schemas import GetStatus, GetPredictionInfo
from app.database_postgres import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/load_image/{prediction_name}", response_model=GetStatus)
async def load_image(
    prediction_name: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    image_service: ImageService = Depends(),
    nn_service: NeuralNetworkService = Depends(),
    dish_service: DishService = Depends(DishService),
    prediction_service: PredictionService = Depends(PredictionService),
):
    mongo_id = await image_service.save_image_to_mongo(file)
    predicted_class = await nn_service.classify_image(mongo_id)
    dish_info = dish_service.get_dish_by_name(predicted_class)
    pred = prediction_service.save_prediction(
        dish_id=dish_info.id, 
        prediction_name=prediction_name, 
        result=predicted_class,
        image_id=mongo_id
    )

    return GetStatus(status="success", id=pred.id)


@router.get("/predict/{predict_id}", response_model=GetPredictionInfo)
def get_prediction_from_service(
    predict_id: int,
    db: Session = Depends(get_db),
    prediction_service: PredictionService = Depends(PredictionService),
    dishes_service: DishService = Depends(DishService),
):
    prediction = prediction_service.get_prediction_by_id(predict_id)
    dish_info = dishes_service.get_dish_by_id(prediction.dish_id)

    return GetPredictionInfo(
        prediction_name=prediction.prediction_name,
        dish_name=dish_info.name,
        calories=dish_info.calories,
        protein=dish_info.protein,
        fat=dish_info.fat,
        carbs=dish_info.carbs,
    )