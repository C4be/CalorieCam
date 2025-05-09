from sqlalchemy.orm import Session
from app.models import Dish, Prediction


class DishRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_dishes(self, skip: int = 0, limit: int = 100):
        return self.db.query(Dish).offset(skip).limit(limit).all()

    def get_dish_by_id(self, dish_id: int):
        return self.db.query(Dish).filter(Dish.id == dish_id).first()
    
    def get_dish_by_name(self, dish_name: str):
        return self.db.query(Dish).filter(Dish.name == dish_name).first()


class PredictionRepository:
    def __init__(self, db: Session):
        self.db = db

    
    def get_all_predictions(self, skip: int = 0, limit: int = 5):
        return self.db.query(Prediction).offset(skip).limit(limit).all()


    def get_prediction_by_id(self, prediction_id: int):
        return self.db.query(Prediction).filter(Prediction.id == prediction_id).first()


    def create_prediction(self, dish_id: int, prediction_name: str, result: str, image_id: str = None):
        new_prediction = Prediction(
            dish_id=dish_id, 
            prediction_name=prediction_name,
            result=result, 
            image_id=image_id
        )
        self.db.add(new_prediction)
        self.db.commit()
        self.db.refresh(new_prediction)
        return new_prediction