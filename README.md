# 📊 Sales Data Processor

ETL-скрипт для обработки CSV-файлов с продажами.

## 🛠 Стек
- Python 3.10+
- pytest
- Standard Library (csv, json, decimal)

## 🚀 Как запустить
```bash
# 1. Клонируй репозиторий
git clone <твой-репо>

# 2. Создай виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Установи зависимости
pip install -r requirements.txt

# 4. Запусти скрипт
python src/processor.py

# 5. Запусти тесты
pytest -v

## 🐳 Запуск в Docker
```bash
# Сборка образа
docker build -t sales-processor .

# Запуск
docker run --rm sales-processor