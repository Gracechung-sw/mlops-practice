import os
from typing import Callable

import numpy as np
from prometheus_client import Histogram # prometheus를 python code로 사용할 수 있도록 만들어놓은 client package가 prometheus_client 이고 여기서 우린 Histogram을 사용할 것임. 
"""
- prometheus_client 의 Histogram 활용
    - [Metric 유형 참고 사이트](https://promlabs.com/blog/2020/09/25/metric-types-in-prometheus-and-promql)  [from PromLabs]
    - bucket : 임의로 지정해 둔 측정 범위를 의미
    - Histogram : bucket 안에 있는 metric 의 빈도 측정
"""
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info
"""
- [info](https://github.com/trallnag/prometheus-fastapi-instrumentator/blob/02e807b76cd2692cf543e207fd07f926a69046d6/prometheus_fastapi_instrumentator/metrics.py#L25) object 에 instrumentation 에 필요한 모든 것이 있음
    - request, response, modified_handler, modified_status, modified_duration 등
"""

NAMESPACE = os.environ.get("METRICS_NAMESPACE", "fastapi")
SUBSYSTEM = os.environ.get("METRICS_SUBSYSTEM", "model")

instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="fastapi_inprogress",
    inprogress_labels=True,
)
## ENABLE_METRICS 가 true 인 Runtime 에서만 동작하게 됨 

# FastAPI 동작의 성능 자체에 대한 metric
instrumentator.add # add method로 수집하고자 하는 metric을 설정함. 
    metrics.request_size( # 요청 size
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.response_size( # 응답 size
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.latency( # 요청에서 응답까지 latency는 얼마나 걸리는지
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.requests( # request 횟수
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)

# model 성능에 대한 metric을 수집해주는 custom metric
def regression_model_output(
    metric_name: str = "regression_model_output",
    metric_doc: str = "Output value of regression model",
    metric_namespace: str = "",
    metric_subsystem: str = "",
    buckets=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, float("inf")),
) -> Callable[[Info], None]:
    METRIC = Histogram(
        metric_name,
        metric_doc,
        buckets=buckets,
        namespace=metric_namespace,
        subsystem=metric_subsystem,
    )

    def instrumentation(info: Info) -> None:
        if info.modified_handler == "/predict":
            predicted_quality = info.response.headers.get("X-model-score")
            if predicted_quality:
                METRIC.observe(float(predicted_quality))

    return instrumentation

buckets = (*np.arange(0, 10.5, 0.5).tolist(), float("inf"))
instrumentator.add(
    # regression_model_output은 instrumentation을 반환하는데, 이건 뭐냐면 Histogram 방식으로 수집하고 있는 predict quality임. 
    # 그리고 이 custom metric을 instrumentator를 더해준다. 
    regression_model_output(metric_namespace=NAMESPACE, metric_subsystem=SUBSYSTEM, buckets=buckets)
)

# 이런식으로 instrumentator가 구성되었다.!