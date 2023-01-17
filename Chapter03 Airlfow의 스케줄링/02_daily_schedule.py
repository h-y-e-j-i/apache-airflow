import datetime as dt

from airflow import DAG

dag = DAG(
    dag_id = "02_daily_schedule",
    schedule_interval = "@daily",
    start_date = dt.datetime(2019, 1, 1)
)