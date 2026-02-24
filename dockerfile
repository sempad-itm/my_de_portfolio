# 1. Базовый образ
FROM python:3.11-slim

# 2. Рабочая директория
WORKDIR /app

# 3. Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем исходный код
COPY src/ ./src/
COPY data/ ./data/
COPY tests/ ./tests/

# 5. Точка входа
ENTRYPOINT ["python", "src/processor.py"]