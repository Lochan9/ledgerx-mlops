from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# === Default configuration ===
default_args = {
    "owner": "lochan",
    "start_date": datetime(2025, 10, 16),
    "retries": 0,
}

# === Define DAG ===
with DAG(
    dag_id="ledgerx_sroie_data_pipeline",
    default_args=default_args,
    description="LedgerX - SROIE Data Pipeline (preprocess + split)",
    schedule_interval=None,  # run manually
    catchup=False,
) as dag:

    # 1️⃣ Preprocessing task
    preprocess = BashOperator(
        task_id="preprocess_sroie",
        bash_command="python /opt/airflow/src/preprocess_sroie.py"
    )

    # 2️⃣ Splitting task
    split = BashOperator(
        task_id="split_sroie",
        bash_command="python /opt/airflow/src/split_data.py"
    )

    # 3️⃣ Optional: DVC push (if remote storage configured)
    dvc_push = BashOperator(
        task_id="dvc_push",
        bash_command="cd /opt/airflow && dvc push",
        trigger_rule="all_done"
    )

    # === Define order ===
    preprocess >> split >> dvc_push
