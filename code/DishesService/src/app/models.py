from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database_postgres import Base

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(
        Integer, primary_key=True, index=True, comment="Уникальный идентификатор блюда"
    )
    name = Column(String, unique=True, index=True, comment="Название блюда")
    calories = Column(Integer, comment="Калорийность блюда (в ккал)")
    protein = Column(Float, comment="Содержание белка (в граммах)")
    fat = Column(Float, comment="Содержание жира (в граммах)")
    carbs = Column(Float, comment="Содержание углеводов (в граммах)")

    predictions = relationship("Prediction", back_populates="dish")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Уникальный идентификатор предсказания",
    )
    dish_id = Column(
        Integer,
        ForeignKey("dishes.id"),
        nullable=False,
        comment="ID блюда, на которое сделано предсказание",
    )
    prediction_name = Column(String, comment="Название предсказания для отображения")
    result = Column(String, comment="Результат предсказания (название класса)")
    image_id = Column(String, nullable=True, comment="ID изображения в MongoDB")

    dish = relationship("Dish", back_populates="predictions")
