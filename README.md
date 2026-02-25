# 📊 Sales Data Processor

ETL-скрипт для обработки CSV-файлов с продажами.

## 🛠 Стек
- Python 3.10+
- pytest
- Standard Library (csv, json, decimal)

## 🐳 Запуск через Docker Compose

### Быстрый старт
```bash
# Запуск всех сервисов (скрипт + PostgreSQL)
docker-compose up --build

# Проверка данных в БД
docker exec -it postgres-etl psql -U etl_user -d etl_db -c "SELECT * FROM reports;"

# Остановка и очистка
docker-compose down -v