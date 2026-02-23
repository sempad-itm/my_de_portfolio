import csv
import json
from decimal import Decimal, InvalidOperation
from datetime import datetime

def read_csv(file) -> list[dict]:
    data = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            data.append(row)
    return data

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

if __name__ == "__main__":

    data = read_csv('data.csv')
    stats = calculate_metrics(data)
    save_json(stats, 'report.json')
    print(f'Отчет готов и сохранен: {stats}')
