# 1. Prerequisites

- k8s 환경
    - minikube v1.22.0
- helm binary
    - helm v3

---

# 2. How to Install

### 1) minikube
```bash
minikube start --driver=docker --cpus='4' --memory='4g'
```
### 2) kube-prometheus-stack Helm Repo 추가

- [https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
- Prometheus, Grafana 등을 k8s 에 쉽게 설치하고 사용할 수 있도록 패키징된 Helm 차트
    - **버전 : kube-prometheus-stack-19.0.2**

```bash
# helm repo 추가
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# helm repo update
helm repo update
```