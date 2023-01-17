from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG(
    dag_id = "01_unscheduled",
    start_date = dt.datetime(2019, 1, 1), # DAG의 시작
    schedule_interval = None,
)

fetch_events = BashOperator(
    task_id = "fetch_events",
    bash_command = (
        "midkr -p /data && "
        "curl -o /data/events.json "
        "http://localhost:5000/events?"
        "start_date=2019-01-01&"        
        "end_date=2019-01-02"
    ),
    dag = dag
)