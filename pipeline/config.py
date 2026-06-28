import os

# SMARD API Configuration
SMARD_BASE_URL = "https://www.smard.de/app/chart_data"
REGION = "DE"
RESOLUTION = "hour"

# Start date for data ingestion
START_DATE = "2025-01-01"

# 10 filters selected for trawa demo
FILTERS = [
    {
        "id": 4169,
        "name": "Market price: Germany/Luxembourg",
        "unit": "EUR/MWh",
        "category": "price"
    },
    {
        "id": 4170,
        "name": "Market price: Austria",
        "unit": "EUR/MWh",
        "category": "price"
    },
    {
        "id": 4067,
        "name": "Power generation: Onshore wind",
        "unit": "MWh",
        "category": "generation"
    },
    {
        "id": 4068,
        "name": "Electricity generation: Photovoltaics",
        "unit": "MWh",
        "category": "generation"
    },
    {
        "id": 1225,
        "name": "Power generation: Offshore wind",
        "unit": "MWh",
        "category": "generation"
    },
    {
        "id": 410,
        "name": "Power consumption: Total (grid load)",
        "unit": "MWh",
        "category": "consumption"
    },
    {
        "id": 4359,
        "name": "Power consumption: Residual load",
        "unit": "MWh",
        "category": "consumption"
    },
    {
        "id": 4071,
        "name": "Electricity generation: Natural gas",
        "unit": "MWh",
        "category": "generation"
    },
    {
        "id": 5097,
        "name": "Projected generation: Wind and photovoltaics",
        "unit": "MWh",
        "category": "forecast"
    },
    {
        "id": 122,
        "name": "Projected production: Total",
        "unit": "MWh",
        "category": "forecast"
    },
]

# MinIO configuration
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_BUCKET = "trawa-energy-lake"

# ClickHouse configuration — no SSL for local
CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = 9002
CLICKHOUSE_DATABASE = "energy"
CLICKHOUSE_USER = "default"
CLICKHOUSE_PASSWORD = ""
CLICKHOUSE_SECURE = False

# Quality check thresholds
MAX_NULL_THRESHOLD = 0.10
MIN_PRICE_EUR_MWH = -500
MAX_PRICE_EUR_MWH = 3000
MIN_MWH = 0
MAX_MWH = 100000
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
