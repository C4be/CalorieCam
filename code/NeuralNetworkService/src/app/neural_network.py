import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras import layers, models
from tensorflow.keras import mixed_precision
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from typing import List, Tuple


class Config:
    """
    Конфигурационный класс для модели нейросети.
    """

    def __init__(
        self,
        img_height: int = 224,
        img_width: int = 224,
        use_fine_tune: bool = True,
        fine_tune_at: int = -50,
        num_classes: int = 101,
        path_to_weights: str = "resources/v1.weights.h5",
        path_to_class_names: str = "resources/class_names.txt",
    ) -> None:
        """
        Args:
            img_height (int): Высота изображения.
            img_width (int): Ширина изображения.
            use_fine_tune (bool): Включить ли fine-tuning.
            fine_tune_at (int): С какого слоя размораживать.
            num_classes (int): Кол-во классов.
            path_to_weights (str): Путь до файла с весами.
            path_to_class_names (str): Путь до файла с названиями классов.
        """
        self.IMG_SIZE: Tuple[int, int] = (img_height, img_width)
        self.IMG_SHAPE: Tuple[int, int, int] = (img_height, img_width, 3)
        self.USE_FINE_TUNE: bool = use_fine_tune
        self.FINE_TUNE_AT: int = fine_tune_at
        self.NUM_CLASSES: int = num_classes
        self.PATH_TO_WEIGHTS: str = path_to_weights
        self.PATH_TO_CLASS_NAMES: str = path_to_class_names


class NeuralNetwork:
    """
    Класс нейросети на базе ResNet50 с возможностью fine-tuning.
    """

    def __init__(
        self,
        img_height: int = 224,
        img_width: int = 224,
        use_fine_tune: bool = True,
        fine_tune_at: int = -50,
        num_classes: int = 101,
        path_to_weights: str = "resources/v1.weights.h5",
        path_to_class_names: str = "resources/class_names.txt",
    ) -> None:
        """
        Инициализирует модель, загружает веса и классы.
        """
        mixed_precision.set_global_policy("mixed_float16")

        self.conf: Config = Config(
            img_height,
            img_width,
            use_fine_tune,
            fine_tune_at,
            num_classes,
            path_to_weights,
            path_to_class_names,
        )
        self.class_names: List[str] = self.load_class_names()
        self.model: tf.keras.Model = self.build_resnet50()

        self.model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )

        if self.load_weights():
            print("Веса загружены!")
        else:
            print("Не удалось загрузить веса!")

        print("TensorFlow version:", tf.__version__)
        print("Num GPUs Available:", len(tf.config.list_physical_devices("GPU")))


    def __repr__(self) -> str:
        """
        Строковое представление модели.
        """
        self.model.summary()
        return f'NN [ResNet50] (IMG[shape={self.conf.IMG_SHAPE}], SETTINGS[num_classes={self.conf.NUM_CLASSES}, fine_tune={"YES" if self.conf.USE_FINE_TUNE else "NO"}])'


    def load_weights(self) -> bool:
        """
        Загружает веса модели, если путь существует.

        Returns:
            bool: Успешно ли загружены веса.
        """
        path: str = self.conf.PATH_TO_WEIGHTS
        if os.path.exists(path):
            self.model.load_weights(path)
            return True
        return False


    def load_class_names(self) -> List[str]:
        """
        Загружает названия классов из текстового файла.

        Returns:
            List[str]: Список названий классов.
        """
        file_path: str = self.conf.PATH_TO_CLASS_NAMES
        if not os.path.exists(file_path):
            print(f"[WARNING] Файл с именами классов не найден: {file_path}")
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return [name.strip() for name in content.split(",") if name.strip()]


    def build_resnet50(self) -> tf.keras.Model:
        """
        Строит архитектуру модели ResNet50.

        Returns:
            tf.keras.Model: Скомпонованная модель.
        """
        base_model: tf.keras.Model = ResNet50(
            weights="imagenet", include_top=False, input_shape=self.conf.IMG_SHAPE
        )

        for layer in base_model.layers:
            layer.trainable = False

        if self.conf.USE_FINE_TUNE:
            for layer in base_model.layers[self.conf.FINE_TUNE_AT :]:
                layer.trainable = True

        model = models.Sequential(
            [
                base_model,
                layers.GlobalAveragePooling2D(),
                layers.Dense(256, activation="relu"),
                layers.Dropout(0.5),
                layers.Dense(
                    self.conf.NUM_CLASSES, activation="softmax", dtype="float32"
                ),
            ]
        )
        return model


    def load_and_preprocess_image(self, img_path: str) -> np.ndarray:
        """
        Загружает и предобрабатывает изображение для предсказания.

        Args:
            img_path (str): Путь к изображению.

        Returns:
            np.ndarray: Обработанный тензор изображения.
        """
        img = image.load_img(img_path, target_size=self.conf.IMG_SIZE)
        img_array = image.img_to_array(img)
        img_array = tf.keras.applications.resnet50.preprocess_input(img_array)
        return np.expand_dims(img_array, axis=0)


    def get_prediction(self, img_path: str) -> int:
        """
        Делает предсказание класса по изображению.

        Args:
            img_path (str): Путь к изображению.

        Returns:
            int: Индекс предсказанного класса.
        """
        img_tensor = self.load_and_preprocess_image(img_path)
        prediction = self.model.predict(img_tensor)
        return int(np.argmax(prediction))
