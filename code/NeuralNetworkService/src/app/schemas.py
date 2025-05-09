from pydantic import BaseModel


class GetPrediction(BaseModel):
    predicted_class: str
