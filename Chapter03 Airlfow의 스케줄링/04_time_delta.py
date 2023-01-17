import datetime as dt

from airflow import DAG

dag = DAG(
    dag_id = "03_with_end_date",
    schedule_interval = dt.timedelta(days=3), # timedelta는 빈도 기반 스케줄을 사용할 수 있는 기능을 제공합니다.
    start_date = dt.datetime(year=2019, month=1, day=1),
    end_date = dt.datetime(year=2019, month=1, day=5)
)