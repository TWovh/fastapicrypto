FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Добавляем Prometheus клиент
RUN pip install prometheus-client

# Копируем код приложения
COPY . .

# Создаем директорию для Prometheus
RUN mkdir -p /tmp

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 