# model-management

## 1. install mlflow
```
pip install mlflow==1.20.2

mlflow --version
# mlflow, version 1.20.2
```

## 2. run MLflow tracking server
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

## 3. train model (quick start)
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

## 4. check mlruns
```bash
cd mlruns/[experiment id]
cd [mlflow run-id]
ls
# artifacs, metrics, params, tag
```

## 5. model serving using mlflow
- using conda for mlflow models serving
- see https://mlflow.org/docs/latest/tutorials-and-examples/tutorial.html for more details
```
mlflfow models serve --help

mlflow models serve -m $(pwd)/mlruns/0/<run-id>/artifacts/model -p <port>

# without conda
mlflow models serve -m $(pwd)/mlruns/0/<run-id>/artifacts/model -p <port> --no-conda
```

## 6. mlflow automatic logging
- mlflow에서 model 관련 log를 확인하는 기능
- see https://github.com/mlflow/mlflow/tree/master/examples/sklearn_autolog for more details
```
python pipeline.py
```

# 7. mlfow metric
- see https://github.com/mlflow/mlflow/tree/master/examples/xgboost for more details
