from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import datetime

dag = DAG("first_workflow", 
            description="First Demo Workflow",
            schedule_interval="0 * * * *",
            start_date=datetime.datetime(2019, 1, 1),
            catchup=False)

def print_first():
    return "Hello"

def print_second():
    return "World"

first_task = PythonOperator(task_id="first_task", dag=dag, python_callable=print_first)
second_task = PythonOperator(task_id="second_task", dag=dag, python_callable=print_second)

first_task >> second_task