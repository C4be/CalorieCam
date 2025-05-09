# CalorieCam V1

## Описание проекта

CalorieCam — это инновационное приложение для распознавания блюд и анализа их пищевой ценности с помощью компьютерного зрения и искусственного интеллекта. Система позволяет пользователям загружать фотографии еды, автоматически определять тип блюда и получать подробную информацию о его калорийности, содержании белков, жиров и углеводов.

### Архитектура проекта

Проект построен на микросервисной архитектуре и состоит из следующих компонентов:

1. **Frontend** — клиентское приложение на Vue.js, предоставляющее пользовательский интерфейс для взаимодействия с системой.

2. **DishesService** — основной сервис, отвечающий за:
   - Прием и обработку запросов от клиента
   - Сохранение изображений в MongoDB
   - Взаимодействие с NeuralNetworkService для классификации изображений
   - Хранение и предоставление информации о блюдах и их пищевой ценности
   - Сохранение результатов предсказаний в PostgreSQL

3. **NeuralNetworkService** — сервис машинного обучения, который:
   - Получает изображения из MongoDB
   - Выполняет классификацию блюд с помощью предобученной нейронной сети
   - Возвращает результаты классификации в DishesService

### Технологический стек

- **Backend**: 
  - FastAPI (Python)
  - SQLAlchemy (ORM для PostgreSQL)
  - MongoDB (хранение изображений)
  - Docker и Docker Compose (контейнеризация)
  
- **Frontend**: 
  - Vue.js
  - Axios (HTTP-клиент)
  - Vite (сборка и разработка)

## Установка и запуск

### Предварительные требования

- Docker и Docker Compose
- Git

### Шаги по установке

1. Клонируйте репозиторий:

```bash
git clone <url-репозитория>
cd CalorieCam
```

2. Запустите приложение с помощью Docker Compose:

```bash
docker-compose up -d
```

Это запустит все необходимые сервисы:
- Frontend на порту 3000
- DishesService на порту 8001
- NeuralNetworkService на порту 8000
- PostgreSQL
- MongoDB

3. Проверьте работу сервисов:

```bash
docker-compose ps
```

### Доступ к приложению

После успешного запуска, приложение будет доступно по адресу:
- Frontend: http://localhost:3000
- DishesService API: http://localhost:8001
- NeuralNetworkService API: http://localhost:8000

## Использование

1. Откройте веб-интерфейс по адресу http://localhost:3000
2. Загрузите фотографию блюда через интерфейс
3. Система автоматически определит тип блюда и отобразит информацию о его пищевой ценности
4. Результаты анализа сохраняются в базе данных и доступны для просмотра в истории

## API-эндпоинты

### DishesService (порт 8001)

- `POST /dish/load_image/{prediction_name}` - Загрузка изображения и получение предсказания
- `GET /dish/predict/{predict_id}` - Получение информации о предсказании по ID

### NeuralNetworkService (порт 8000)

- `GET /nn/predict/{image_id}` - Получение предсказания по ID изображения
- `GET /nn/classes` - Получение списка всех доступных классов блюд

## Очистка и остановка

Для остановки всех сервисов:

```bash
docker-compose down
```

Для полной очистки (включая удаление томов с данными):

```bash
docker-compose down -v
```

## Структура проекта

```
CalorieCam/
├── code/
│   ├── DishesService/
│   │   └── src/
│   │       ├── app/
│   │       │   ├── endpoints.py
│   │       │   ├── repositories.py
│   │       │   ├── schemas.py
│   │       │   ├── services.py
│   │       │   ├── database_postgres.py
│   │       │   ├── database_mongo.py
│   │       │   └── init_db.py
│   │       ├── main.py
│   │       ├── requirements.txt
│   │       └── Dockerfile
│   ├── NeuralNetworkService/
│   │   └── src/
│   │       ├── app/
│   │       │   ├── endpoints.py
│   │       │   ├── services.py
│   │       │   ├── neural_network.py
│   │       │   └── database_mongo.py
│   │       ├── main.py
│   │       ├── requirements.txt
│   │       └── Dockerfile
│   └── frontend/
│       ├── src/
│       ├── package.json
│       └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Разработка

### Локальный запуск сервисов

Для локальной разработки можно запустить каждый сервис отдельно:

#### DishesService:

```bash
cd code/DishesService/src
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

#### NeuralNetworkService:

```bash
cd code/NeuralNetworkService/src
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend:

```bash
cd code/frontend
npm install
npm run dev
```

### Настройка для разработки

При локальной разработке необходимо изменить URL-адреса сервисов в конфигурационных файлах:

- В `DishesService/src/app/services.py` раскомментировать строку с локальным URL:
  ```python
  self.nn_service_url = "http://localhost:8000/nn/predict"
  # self.nn_service_url = "http://caloriecam-nn-service:8000/nn/predict"
  ```


## Шаги для запуска всех сервисов

1. Убедитесь, что у вас установлены необходимые предварительные требования:
   - Docker
   - Docker Compose
   - Git

2. Перейдите в корневую директорию проекта CalorieCam:
   ```bash
   cd CalorieCam
   ```

3. Запустите все сервисы с помощью Docker Compose:
   ```bash
   docker-compose up -d
   ```

   Флаг `-d` запускает контейнеры в фоновом режиме (detached mode).

4. Проверьте статус запущенных сервисов:
   ```bash
   docker-compose ps
   ```

# Обучение нейросети


Файл `/Users/cube/Desktop/Софья/CalorieCam/Maсhine_learning.ipynb` представляет собой Jupyter Notebook, который содержит код для обучения модели машинного обучения, используемой в проекте CalorieCam для распознавания блюд.

## Основные компоненты

### Используемые библиотеки
- TensorFlow и Keras для создания и обучения нейронной сети
- TensorFlow Datasets для загрузки набора данных Food101
- NumPy для работы с массивами
- Mixed Precision для оптимизации вычислений на GPU

### Архитектура модели
- Используется предобученная модель ResNet50 с весами ImageNet
- Применяется техника transfer learning с fine-tuning последних 50 слоев
- Добавлены дополнительные слои:
  - GlobalAveragePooling2D
  - Dense (256 нейронов с активацией ReLU)
  - Dropout (0.5)
  - Выходной слой с 101 классом (по количеству типов блюд)

### Набор данных
- Используется датасет Food101, содержащий 101 класс различных блюд
- Данные разделены на:
  - Тренировочный набор (80% от исходного train)
  - Валидационный набор (20% от исходного train)
  - Тестовый набор (исходный validation)

### Параметры обучения
- Размер изображений: 224x224 пикселей
- Размер батча: 32
- Количество эпох: 5
- Используется аугментация данных (горизонтальное и вертикальное отражение)
- Применяется оптимизатор Adam
- Функция потерь: sparse_categorical_crossentropy

### Сохранение модели
- Веса модели сохраняются в файл 'v1.weights.h5' на Google Drive
- Используется ModelCheckpoint для сохранения лучшей модели по метрике val_loss
- Список классов сохраняется в файл 'classes.txt'

## Интеграция с CalorieCam

Данная модель является ключевым компонентом NeuralNetworkService в архитектуре CalorieCam. После обучения модель используется для классификации изображений блюд, загруженных пользователями через интерфейс приложения.

Обученная модель способна распознавать 101 тип блюд и предоставлять информацию о них, которая затем используется для расчета пищевой ценности в основном сервисе приложения.

        