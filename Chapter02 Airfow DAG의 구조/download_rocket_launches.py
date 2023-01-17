import json
import pathlib

import airflow
import requests
import requests.exceptions as request_exception
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# DAG 클래스는 두 개의 인수가 필요
dag = DAG( # 모든 워크플로의 시작점
    dag_id = "download_rocket_launches", # Airlfow UI에 표시되는 DAG 이름
    start_date = airflow.utils.dates.days_ago(14), # 워크플로가 처음 실행되는 날짜/시간
    schedule_interval = None, # DAG 실행 간격
)

download_launches = BashOperator( # BashOperator를 이용해 curl로 URL 결과값 다운로드
    task_id="download_launches", # 태스크 이름
    bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'", # 실행할 배시 커맨드
    dag = dag,
)

# 파이썬 함수는 결과값을 파싱하고 모든 로켓 사진을 다운로드
def _get_pictures(): # 호출할 파이썬 함수
    # 경로가 존재하는지 확인
    pathlib.Path('tmp/images').mkdir(parents=True, exist_ok=True) # 경로가 없으면 디렉터리 생성

    # launches.json 파일에 있는 모든 그림 파일을 다운로드
    with open("tmp/launchs.json") as f: # 로켓 발사 JSON 파일 열기
        launches = json.load(f) # 데이터를 섞을 수 있도록 딕셔너리로 읽기
        image_urls = [launch["image"] for launch in launches["result"]] # 모든 발사에 대한 'image'의 URL 값 읽기
        # 모든 이미지 URL을 얻기 이ㅜ한 루프
        for image_url in image_urls:
            try:
                response = requests.get(image_url) # 이미지 가져오기
                image_filename = image_url.split("/")[-1] # 마지막 파일 이름만 가져오기
                target_file = f"/tmp/images/{image_filename}" # 타겟 파일 저장 경로 구성
                with open(target_file, "wb") as f: # 타겟 파일 핸들 얻기
                    f.write(response.content) # 각각의 이미지 저장
                print(f"Downloaded {image_url} to {target_file}") # Airflow 로그에 저장하기 위해 stdout으로 출력
            # 잠재적인 에러 포착 및 처리
            except request_exception.MissingSchema:
                print(f"{image_url} appears to be an invalid URL.")
            except request_exception.ConnectionError:
                print(f"Could not connect to {image_url}")

get_pictures = PythonOperator( # 파이썬 함수 호출을 위해 PythonOperator 구체화
    task_id = "get_pictures",
    python_callable = _get_pictures, # DAG에서 PythonOperator를 사용하여 파이썬 함수 호출
    dag = dag
)

notify = BashOperator(
    task_id = "notify",
    bash_command = 'echo "There are now $(ls /tmp/images/ | wc -l) images."', # 실행할 파이썬 함수를 지정
    dag = dag
)

download_launches >> get_pictures >> notify # 화살표(>>)는 태스크 실행 순서를 결정

