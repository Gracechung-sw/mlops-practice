# Model CICD pipeline

## Github Actions와 CML 과 DVC 연계를 통한 Model Metric Tracking
실습 목표
1. Github Actions 를 활용하여 예제 머신러닝 코드 실행하여 성능 지표 출력하기
2. CML 을 사용하여 성능 지표를 레포트 형태로 출력하기
3. 분석 코드 변경 후 재배포 시 레포트 재생성 하기
4. DVC 를 활용하여 Metric 의 변화 추적하기

- Github Actions: 개발자의 workflow를 자동화 시키기 위한 platform (주의. CICD tool 이 아님. CICD도 workflow 중 하나일 뿐임.)
- [CML](https://github.com/iterative/cml) : 데이터 사이언스 프로젝트를 지속적으로 통합시키기 위한 오픈소스
- [DVC](https://dvc.org/): Data management tool이며 이것에 대한 자세한 내용은 ./data-management/README.md 에 적어둔 바 있다. 

### Let's run in local env
```bash
python3 -m venv venv && source ./venv/bin/activate

pip install -r requirements.txt

python3 train.py

# after train is done, check output files feature_importance.png, residuals.png, metrics.txt(성능지표). 
```


### CML 을 사용하여 성능 지표를 레포트 형태로 출력하기
Github Actions에서 실행되어서 출력된 결과를 Github Actions console page에 들어가지 않고 레포트 형식으로 출력된 것을 볼 수 있도록 CML을 사용해보자. 

- [CML Functions](https://github.com/iterative/cml#cml-functions) 에서 
  - cml-publish: Publish host an image for displaying in a CML report.
  - cml-send-comment: 
  를 사용해보고자함. 
## Jenkinsfile을 이용한 CI Pipeline 빌드

## Python기반 Jenkins CI Piepline 생성


