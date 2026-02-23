import pytest
from src.processor import calculate_metrics

def test_basic_revenue():
    """Проверка правильности подсчета выручки"""
    rows = [{'product': 'Apple', 'price': 10, 'quantity': 2},
           {'product': 'Banana', 'price': 25, 'quantity': 10}]
    
    result = calculate_metrics(rows)
    assert result['total_revenue'] == 270.00
    assert result['processed_rows'] == 2

def test_anomaly_filtered():
    """Проверка правильности подсчета аномалий"""
    rows = [{'product': 'Apple', 'price': -10, 'quantity': 2},
           {'product': 'Banana', 'price': 25, 'quantity': -10},
           {'product': 'Banana', 'price': 25, 'quantity': 10}]
    
    result = calculate_metrics(rows)
    assert result['total_revenue'] == 250
    assert result['filtered_anomalies'] == 2