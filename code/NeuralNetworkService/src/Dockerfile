FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
COPY requirements_tf_windows_cuda.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_tf_windows_cuda.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]