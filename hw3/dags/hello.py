import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
# from airflow.operators.

with DAG(
    dag_id="hello_world",
    start_date=datetime.datetime(2021, 1, 1),
    schedule=None,
):
    EmptyOperator(task_id="task")