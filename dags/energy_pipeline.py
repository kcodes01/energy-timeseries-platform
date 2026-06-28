from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import sys
import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_slack(message: str, color: str = "good"):
    requests.post(SLACK_WEBHOOK_URL, json={
        "attachments": [{
            "color": color,
            "text": message
        }]
    })

def on_failure_callback(context):
    task_id = context['task_instance'].task_id
    dag_id = context['dag'].dag_id
    error = str(context.get('exception', 'Unknown error'))
    send_slack(
        f"🔴 *Airflow Task Failed*\n"
        f"• DAG: {dag_id}\n"
        f"• Task: {task_id}\n"
        f"• Error: {error[:200]}",
        color="danger"
    )

def on_success_callback(context):
    task_id = context['task_instance'].task_id
    send_slack(
        f"✅ *Task Completed*: {task_id}",
        color="#36a64f"
    )

default_args = {
    'owner': 'kaleab',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'on_failure_callback': on_failure_callback,
}

def run_smard_pipeline():
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
    result = subprocess.run(
        ["dbt", "run",
         "--project-dir", "/opt/airflow/dbt_project",
         "--profiles-dir", "/opt/airflow/dbt_project"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")

def run_dbt_test():
    result = subprocess.run(
        ["dbt", "test",
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
    schedule_interval="0 6 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["energy", "smard", "dlt", "dbt"],
) as dag:

    ingest = PythonOperator(
        task_id="ingest_smard_data",
        python_callable=run_smard_pipeline,
        on_success_callback=on_success_callback,
    )

    transform = PythonOperator(
        task_id="dbt_transform",
        python_callable=run_dbt_run,
        on_success_callback=on_success_callback,
    )

    test = PythonOperator(
        task_id="dbt_test",
        python_callable=run_dbt_test,
        on_success_callback=on_success_callback,
    )

    ingest >> transform >> test
