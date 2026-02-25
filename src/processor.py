import csv
import json
from decimal import Decimal, InvalidOperation
from datetime import datetime
from pathlib import Path
import psycopg2
import time
from typing import Dict

def read_csv(file) -> list[dict]:
    csv_data = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            csv_data.append(row)
    return csv_data

def calculate_metrics(rows:list) -> dict:
    total_revenue = Decimal('0.0')
    revenue_products = {}
    processed_rows = 0
    top_product = ''
    filtered_anomalies = 0
    generated_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    for row in rows:
        try:
            price = Decimal(row['price'])
            quantity = int(row['quantity'])

            if price < 0 or quantity <= 0:
                filtered_anomalies += 1
                continue

            revenue = price * quantity
            total_revenue += revenue
            revenue_products[row['product']] = revenue_products.get(row['product'], Decimal('0')) + revenue
            processed_rows += 1

        except (ValueError, InvalidOperation):
            filtered_anomalies += 1
            continue

    if revenue_products:
        top_product = max(revenue_products, key=revenue_products.get)
        
    return {'total_revenue':float(total_revenue), 'top_product':top_product,
            'processed_rows':processed_rows, 'filtered_anomalies':filtered_anomalies,
            'generated_at':generated_at}

def save_json(data: dict, filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def connect_to_db(db_config: Dict, max_retries: int = 15, delay: int = 2):
    """
    Пытается подключиться к БД с повторными попытками.
    Это нужно, потому что PostgreSQL стартует дольше, чем твой скрипт.
    """
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password']
            )
            print(f"✅ Подключение к БД успешно (попытка {attempt + 1}/{max_retries})")
            return conn
        except psycopg2.OperationalError as e:
            print(f"⚠️ Попытка {attempt + 1}/{max_retries} не удалась: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Ждем {delay} секунд перед следующей попыткой...")
                time.sleep(delay)
            else:
                print("❌ Все попытки исчерпаны. Завершаем работу.")
                raise  # Пробрасываем ошибку дальше

def save_to_postgres(data, db_config: Dict):  # ✅ Параметр называется data
    """Сохраняет метрики в PostgreSQL"""
    conn = connect_to_db(db_config)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO reports (total_revenue, top_product, processed_rows, filtered_anomalies, generated_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data['total_revenue'],      # ✅ Обращаемся к параметру функции
        data['top_product'],
        data['processed_rows'],
        data['filtered_anomalies'],
        data['generated_at']
    ))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Данные успешно сохранены в PostgreSQL")

if __name__ == "__main__":
    # Читаем конфиг из env-переменных (как в Docker)
    import os
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'dbname': os.getenv('DB_NAME', 'etl_db'),
        'user': os.getenv('DB_USER', 'etl_user'),
        'password': os.getenv('DB_PASSWORD', 'etl_password')
    }
    # ETL-логика
    BASE_DIR = Path(__file__).parent.parent
    csv_data = read_csv(BASE_DIR / 'data' / 'data.csv')
    stats = calculate_metrics(csv_data)
    print(f"🔍 Тип stats: {type(stats)}")
    print(f"📈 Метрики: {stats}")

     # Сохраняем в БД (если конфиг задан)
    if db_config['host']:
        save_to_postgres(stats, db_config)
        print(f"✅ Данные сохранены в PostgreSQL: {db_config['host']}")
    else:
        save_json(stats, BASE_DIR / 'report.json')
        print(f"📄 Отчет сохранен в JSON")
