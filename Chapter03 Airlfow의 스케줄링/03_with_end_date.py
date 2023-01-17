import datetime as dt

from airflow import DAG

dag = DAG(
    dag_id = "03_with_end_date",
    schedule_interval = "@daily",
    start_date = dt.datetime(year=2019, month=1, day=1),
    end_date = dt.datetime(year=2019, month=1, day=5)
)