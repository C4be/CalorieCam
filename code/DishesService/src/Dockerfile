FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей для psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Заменяем psycopg2 на psycopg2-binary в requirements.txt, если он там есть
RUN if grep -q "psycopg2" requirements.txt; then \
    sed -i 's/psycopg2/psycopg2-binary/g' requirements.txt; \
    fi
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]