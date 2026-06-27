from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import subprocess
import sys

default_args = {
    'owner': 'kaleab',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}

def run_smard_pipeline():
    """Run dlt pipeline — fetch SMARD data → MinIO + ClickHouse."""
    result = subprocess.run(
        [sys.executable, "/opt/airflow/pipeline/smard_pipeline.py"],
        capture_output=True,
        text=True,
        cwd="/opt/airflow/pipeline"
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Pipeline failed: {result.stderr}")

def run_dbt_run():
    """Run dbt models."""
    result = subprocess.run(
        ["/opt/airflow/venv/bin/dbt", "run",
         "--project-dir", "/opt/airflow/dbt_project",
         "--profiles-dir", "/opt/airflow/dbt_project"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")

def run_dbt_test():
    """Run dbt tests."""
    result = subprocess.run(
        ["/opt/airflow/venv/bin/dbt", "test",
         "--project-dir", "/opt/airflow/dbt_project",
         "--profiles-dir", "/opt/airflow/dbt_project"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt test failed: {result.stderr}")

with DAG(
    dag_id="energy_timeseries_pipeline",
    description="Daily energy market data pipeline: SMARD → MinIO → ClickHouse → dbt",
    default_args=default_args,
    schedule_interval="0 6 * * *",  # runs daily at 6am
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["energy", "smard", "dlt", "dbt"],
) as dag:

    ingest = PythonOperator(
        task_id="ingest_smard_data",
        python_callable=run_smard_pipeline,
        doc_md="""
        Fetches energy market data from SMARD API for 10 filters.
        Normalizes with polars, runs quality checks,
        saves Parquet to MinIO, loads to ClickHouse via dlt.
        """
    )

    transform = PythonOperator(
        task_id="dbt_transform",
        python_callable=run_dbt_run,
        doc_md="""
        Runs dbt models:
        - staging: stg_energy_timeseries
        - intermediate: int_hourly_prices, int_renewable_generation, int_residual_load
        - marts: mart_daily_price_summary, mart_capture_prices, mart_flexibility_signals
        """
    )

    test = PythonOperator(
        task_id="dbt_test",
        python_callable=run_dbt_test,
        doc_md="Runs dbt data quality tests on all models."
    )

    # Pipeline order
    ingest >> transform >> test
