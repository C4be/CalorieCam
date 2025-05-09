from pydantic import BaseModel

class GetPredictionInfo(BaseModel):
    prediction_name: str
    dish_name: str
    calories: int
    protein: float
    fat: float
    carbs: float
    
class GetStatus(BaseModel):
    status: str
    id: int
