# Model Management

## Intro
### 1. Model Management의 필요성
model 개발 과정을 보면
Data Processing -> Train & Evaluate -> Raw Data -> 다시 Data Processing....

과정의 반복이다. 

그리고 Production level로 AI model이 serving되고 그 이후에 성능 개선이 되어서 version up 된 model이 serving되기도 한다. 
아니면 아직 serving되기 전에도 여러 성능비교를 하며 model version이 update되기도 한다. 

> AI 회사에 다니면서 백엔드 개발자로서 한 역할 중에 model serving 및 AI model Inference server 개발을 맡은 적이 있고, 
model version을 client요청에 맞게 동적으로 변경시켜가며 inference할 수 있는 서버 구조가 필요했다.       
> 이를 위해서 개발팀은   
   >>  - 요청이 온 model type, version에 맞게 GPU AI Inference server에 AI model이 동적으로 plugin처럼 load/unload되어서 요청을 처리할 수 있도록 architecture을 디자인하고 개발하는 것이 필요하고
   >>  - AI model update시마다 분석 결과의 이상치 test code
   >>  - 성능 test code 
   >>  - CI로 해당 test 자동화
   
> 연구팀은    
    >> - model 성능 개선에 따른 versioning관리
    >> - model version upgrade에 따른 release시 release note 작성

> 를 맡아야 한다.   
말이 길어졌는데, 아무튼 현업에서의 model versioning관련해서 경험한 것을 적으려고 했다.   


Model 결정시 어떤 data 저장이 필요한가
- model 소스 코드
- Evaluation Metric 결과
- 사용한 parameters
- model.pkl 파일
- 학습에 사용한 data
- 데이터 전처리용 코드
- 전처리된 data
... 등

이런 정보들이 함께 저장되어야 추후에 '해당 모델의 성능을 **재현** 할 수 있다.'

이런 데이터의 저장 방식이 통일되지 않고, 수동으로 한다면 실수가능성이 매우 높다. 
어려움을 리스트업 해보면
- 비슷한 작업이 반복적으로 일어난다. 
- Dependency 패키지들이 많으며, 버전 관리가 어렵다. 
- 사람 Dependency가 생긴다. 이는 실수로 이어진다. 
- 테스트하기 어렵다. 
- Reproduce되지 않는 경우가 많다. 
- Model 학습용 코드를 구현하는 사람(연구팀이 될 수 있고)과 Serving용 코드를 구현하는 사람(개발팀이 될 수 '도' 있다.)이 분리되어있다. 

이를 도와주는 Tool이 Model Management(model tracking) Tool들이 많이 나왔다. 대표적으로 `MLflow`, `Weight & Biases`, `Tensorboard`, `Neptune`, `Comet.m`l등이 있다. 

이 중에서 **MLflow**에 대해서 알아보고자 한다.  

### MLflow
MLflow 구성요소
- `mlflow tracking`: model의 hyperparameter나 source code를 변경시켜가며 test할 때 각각의 model version의 metric을 저장하는 중앙 저장소를 제공하고 meta정보와 model을 저장할 수 있도록 python api를 제공한다. 
- `mlflow projects`: model 학습 코드의 성능을 재현할 수 있도록 parameter에 model에 의존성이 있는 모든 정보(ex. package version정보 등)을 함께 넣어서 코드를 packaging해주는 것을 말함
- `mlflow models`: model을 R로 개발했든 pytorch로 개발했든 tensorflow로 했든 특정 framework에 종속되지 않고 항상 통일된 형태로 배포에 사용할 수 있도록 format화 시켜주는 기능
- `mlflow model registry`: mlflow에 실험했던 model을 저장하고 관리하는 저장소. 

여기서는 **MLflow tracking 기능**에 대해서 알아보고자 한다.



---

## Install mlflow
```
pip install mlflow==1.20.2

mlflow --version
# mlflow, version 1.20.2
```

---
## Run MLflow tracking server
 - check command options
```bash
mlflow ui --help

mlflow server --help
```

- 학습을 위해서 mlflow ui로 띄우기

```bash
cd model-management

mlflow ui
```

- `mlruns` directory added 
    - `mlflow ui` 실행 시 `--backend-store-uri`, `--default-artifact-root` 옵션을 주지 않은 경우, `mlflow ui` 를 실행한 디렉토리에 `mlruns` 라는 디렉토리를 생성한 뒤, 이 곳에 실험 관련 데이터를 저장하게 됩니다.

---

## Train model (quick start)
- example code
    - from https://raw.githubusercontent.com/mlflow/mlflow/master/examples/sklearn_elasticnet_diabetes/osx/train_diabetes.py
    -  uses the scikit-learn diabetes dataset and predicts the progression metric (a quantitative measure of disease progression after one year) based on BMI, blood pressure, and other measurements. It uses the scikit-learn ElasticNet linear regression model, varying the alpha and l1_ratio parameters for tuning. For more information on ElasticNet, refer to:
        -  Elastic net regularization
        - Regularization and Variable Selection via the Elastic Net
    - see https://docs.databricks.com/_static/notebooks/mlflow/mlflow-quick-start-training.html for more details.
```bash
cd model-management

python train_diabetes.py
```
- and check updated mlflow ui.

---

## Check mlruns
```bash
cd mlruns/[experiment id]
cd [mlflow run-id]
ls
# artifacs, metrics, params, tag
```

---
## Model serving using mlflow
- using conda for mlflow models serving
- see https://mlflow.org/docs/latest/tutorials-and-examples/tutorial.html for more details
```
mlflfow models serve --help

mlflow models serve -m $(pwd)/mlruns/0/<run-id>/artifacts/model -p <port>

# without conda
mlflow models serve -m $(pwd)/mlruns/0/<run-id>/artifacts/model -p <port> --no-conda
```

---

## Mlflow automatic logging
- mlflow에서 model 관련 log를 확인하는 기능
- see https://github.com/mlflow/mlflow/tree/master/examples/sklearn_autolog for more details
```
python pipeline.py
```
---
## Mlfow metric
- see https://github.com/mlflow/mlflow/tree/master/examples/xgboost for more details
