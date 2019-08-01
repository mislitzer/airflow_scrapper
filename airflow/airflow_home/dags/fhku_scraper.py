import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

dag = DAG("fhku_scraping_workflow", 
            description="Scraping Event from FH Kufstein Website",
            schedule_interval="0 * * * *",
            start_date=datetime.datetime(2019, 1, 1),
            catchup=False)

prepare_db_task = BashOperator(
    task_id="prepare_db_task",
    bash_command="python3 /Users/martin/dev1/fh/FH/MSc/03_sew/scrapping/declarations.py",
    dag=dag
)

scraping_task = BashOperator(
    trigger_rule="one_success",
    task_id="scraping_task",
    bash_command="python3 /Users/martin/dev1/fh/FH/MSc/03_sew/scrapping/main.py",
    dag=dag
)

prepare_db_task >> scraping_task