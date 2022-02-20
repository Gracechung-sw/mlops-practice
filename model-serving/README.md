I have a model, now what?
model serving: ML Model을 서비스화 하는 것. 사용자가 어떤 방식으로든 input data를 넣으면 그에 대한 결과를 '어떤 방식으로든' output해주는 것. 


- input을 주는 방식
    source는 
    - HTTP API Request
    - 챗봇과의 대화
    - Netflix 영상 좋아요 버튼
    - Youtube 구독 버튼
    - 네이버 출발, 도착지를 입력한 후 길찾기 버튼
    ... 가 될 수도 있고, 

    - Batch, 
    - Stream..등으로 나눠볼 수도 있다. 

- Model Serving이 어려운 이유
    - Model Serving은 model의 predict 함수를 call 하는 로직이 들어간 SW를 개발 하는 것인데.. 
        - 모델 개발과 소프트웨어 개발 방법의 괴리
        - 모델 개발과정과 소프트웨어 개발 과정의 파편화
        - 모델 평가 방식 및 모니터링 구축의 어려움. 

    - ML Model Serving tool
        - Seldon Core
        - TFServing
        - KFServing
        - Torch Serve
        - BentoML
        하지만 Python기반의 REST API Framework를 사용해서 머신러닝 코드를 감싼 API server를 개발하고, 
        해당 API server를 dockerize한 뒤에 배포하는 식을 사용하기도 한다. 

---
## Start
```bash
cd mlops-practice/model-serving
conda activate mlops-prac
```

## Prepare model to serve
- iris data 를 사용한 간단한 classification model 을 학습한 뒤, 모델을 pickle 파일로 저장하고, Flask 를 사용해 해당 파일을 load 하여 predict 하는 server 를 구현할 것입니다.
- 그 이후, 해당 server 를 run 하여 직접 http request 를 요청하여 정상적으로 response 가 반환되는지 확인할 것입니다.
```bash
python train_save_model.py
```


## Using Flask for model serving
### 1. Flask 란

> The python micro framework for building web applications
- [https://github.com/pallets/flask](https://github.com/pallets/flask)
> 

- Micro Service Architecture (MSA) 를 위한 web app framework
    - web app framework (web framework) : 웹 서비스 개발을 위한 프레임워크
- Django 등 다른 framework 에 비해 굉장히 가벼우며, 확장성, 유연성이 뛰어난 프레임워크
    - 단, 자체 지원 기능은 적다는게 장점이자 단점

- 사용하기 쉽고, 간단한 기능을 가볍게 구현하기에 적합하기 때문에 대부분의 ML Model 의 첫 배포 Step 으로 Flask 를 자주 사용합니다.


### 2. Flask 설치

- Prerequisite
    - Python 가상환경
        - 3.6 이상
            - 3.8.9 사용
        - pip3
- How to Install
```bash
# Flask 설치
pip install -U Flask==2.0.2

# Flask Version 확인
conda list
```

### 3. 모델 학습 및 저장
see train_save_model.py

### 4. Flask model server 구현
1.에서 학습 후 저장했던 모델(pickle 파일)을 load 하여, POST /predict API 를 제공하는 Flask Server 를 구현합니다.
see flask_model_server.py

### 5. API 테스트
```bash
curl -X POST -H "Content-Type:application/json" --data '{"sepal_length": 5.9, "sepal_width": 3.0, "petal_length": 5.1, "petal_width": 1.8}' http://localhost:5000/predict

# {"result":[2]}
# 0, 1, 2  중의 하나의 type 으로 classification 하게 됩니다.
```