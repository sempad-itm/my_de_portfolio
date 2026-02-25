CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    total_revenue NUMERIC(12, 2) NOT NULL,
    top_product TEXT NOT NULL,
    processed_rows INTEGER NOT NULL,
    filtered_anomalies INTEGER NOT NULL,
    generated_at TIMESTAMP DEFAULT NOW()
);

-- Индекс для ускорения поиска по дате
CREATE INDEX IF NOT EXISTS idx_reports_generated_at ON reports(generated_at);