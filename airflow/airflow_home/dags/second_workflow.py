import datetime
import logging
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator

log = logging.getLogger(__name__)

dag = DAG("second_workflow", 
            description="Second Demo Workflow",
            schedule_interval="0 * * * *",
            start_date=datetime.datetime(2019, 1, 1),
            catchup=False)

def print_start():
    log.info("START")

def print_end():
    log.info("END")

def week():
    log.info("execute week TASK")

def weekend():
    log.info("execute weekend TASK")

def branch(**context):
    weekday = context["ti"].xcom_pull(key="weekday", task_ids="check_weekday_task")
    if weekday in (5, 6):
        return "weekend_task"
    else:
        return "week_task"

def check_weekday(**context):
    context["ti"].xcom_push("weekday", datetime.datetime.today().weekday())

branch_task = BranchPythonOperator(provide_context=True, task_id="branch_task", python_callable=branch, dag=dag)
check_weekday_task = PythonOperator(provide_context=True, task_id="check_weekday_task", python_callable=check_weekday, dag=dag)
start_task = PythonOperator(task_id="start_task", python_callable=print_start, dag=dag)
end_task = PythonOperator(trigger_rule="one_success", task_id="end_task", python_callable=print_end, dag=dag)
week_task = PythonOperator(task_id="week_task", python_callable=week, dag=dag)
weekend_task = PythonOperator(task_id="weekend_task", python_callable=weekend, dag=dag)

start_task >> check_weekday_task >> branch_task >> [week_task, weekend_task] >> end_task