# Pipeline Monitoring

## Pipeline Monitoring Architecture
![pipeline monitoring](../assets/img/pipeline-monitoring.png)

1. 데이터: [Red Wine Quality data](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009)
2. code: 표준화 하는 코드와 모델링 하는 코드가 있음. 
3. Joblib artifacts: 표준화 code를 실행 하면 scaler 가 나오고, 모델링 code를 실행하면 모델 파일이 나온다. 이 둘을 [Joblib artifacts](https://joblib.readthedocs.io/en/latest/) 형식으로 저장. 
4. Serving API: Fast API와 Pydantic을 사용해서 Serving API를 구현함.  (Pydantic: pydantic : Type annotations 을 사용해 데이터 구문 분석 및 유효성 검사를 자동으로 해주고 오류 시 error 를 반환해주는 유용한 라이브러리)
5. Github에 push
6. Jenkins: Build App and Run. 이때 Build된 docker image를 Docker hub에 push
7. Container를 실행하고 
8. Locust: 생성된 docker container에서 실행되고 있는 App을 테스트 
9. Prometheus: Jenkins의 동작의 metric을 수집, Locust가 App을 실행할 때의 metrics을 수집. 
10. Grafana: Jenkins에서 수집한 metric은 Jenkins monitoring dashboard에, Locust에서 실행된 App의 metric을 ML 모델 성능 Monitoring dashboard에 표현해줌. 

-> 결과적으로 Jenkins monitoring 과 ML 모델 성능 Monitoring이 있는데 ML 모델 성능 Monitoring에 대해서 실습을 진행해본다. 

## 실습 주제
### Prerequisite
1. Data 준비. [Red Wine Quality data](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009)에서 csv download
2. train.py 에 간단한 모델 훈련 코드 생성
3. 실행하여 모델 joblib artifact, scaler joblib artifact 생성
```bash
python3 -m venv venv && source ./venv/bin/activate 

pip install -r requirements.txt 

python train.py

# result
# INFO:__main__:Preparing dataset...
# INFO:__main__:Training model...
# INFO:__main__:Test MSE: 0.35108395857445623
# INFO:__main__:Saving artifacts...
```

### 실습 1. ML 모델 성능 Monitoring
1. FastAPI Serving API 생성
    - schemas.py: Data Validation 을 위한 [pydantic schema](https://pydantic-docs.helpmanual.io/usage/schema/) 작성
    - app.py: 패키지, scaler, model 로드, 기본 api 생성
    - 실행을 위해 Dockerfile, docker-compose file 작성. 
2. FastAPI Serving API(ML Serving App) 실행
```bash
docker-compose up

# Go localhost:5000
```
3. FastAPI-Prometheus Metric 수집
    - FastAPI와 Prometheus을 연결하는 [prometheus_fastapi_instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator) 사용
4. Prometheus 와 Grafana 연동
5. Locust를 이용한 Simulation 및 Dashboard 생성
### 실습 2. Jenkins 를 이용한 ML 모델 업데이트 및 자동 배포
### 실습 3. Jenkins Monitoring

을 진행해 볼 것임. 

각각의 실습마다 별도의 markdown 정리와 example code, config file 들이 생성 될 것이며 링크를 첨부할 예정. 
