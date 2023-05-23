import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
# from airflow.operators.

with DAG(
    dag_id="hello_world",
    start_date=datetime.datetime(2021, 1, 1),
    schedule=None,
):
    EmptyOperator(task_id="task")
    prepare_dir = BashOperator(
        task_id="prepare_dir",
        bash_command="echo 'hello from hello world'"
    )
