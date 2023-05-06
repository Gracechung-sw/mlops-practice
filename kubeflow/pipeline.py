from kfp.components import create_component_from_func

"""
kfp.components.create_component_from_func 이란:
    Python 함수를 Component 로 바꿔주는 함수
    decorator 로도 사용할 수 있으며, 여러 옵션을 argument 로 설정할 수 있음
    
    add_op = create_component_from_func(
                func=add,
                base_image='python:3.7', # Optional : component 는 k8s pod 로 생성되며, 해당 pod 의 image 를 설정
                output_component_file='add.component.yaml', # Optional : component 도 yaml 로 compile 하여 재사용하기 쉽게 관리 가능
                packages_to_install=['pandas==0.24'], # Optional : base image 에는 없지만, python code 의 의존성 패키지가 있으면 component 생성 시 추가 가능
            )
"""

def add(value_1: int, value_2: int) -> int:
    """
    더하기
    """
    ret = value_1 + value_2
    return ret

def subtract(value_1: int, value_2: int) -> int:
    """
    빼기
    """
    ret = value_1 - value_2
    return ret

def multiply(value_1: int, value_2: int) -> int:
    """
    곱하기
    """
    ret = value_1 * value_2
    return ret

# Python 함수를 선언한 후, kfp.components.create_component_from_func 를 사용하여
# ContainerOp 타입(component)으로 convert
add_op = create_component_from_func(add)
subtract_op = create_component_from_func(subtract)
multiply_op = create_component_from_func(multiply)

from kfp.dsl import pipeline

@pipeline(name="add example")
def my_pipeline(value_1: int, value_2: int):
    task_1 = add_op(value_1, value_2)
    task_2 = subtract_op(value_1, value_2)

    # component 간의 data 를 넘기고 싶다면,
    # output -> input 으로 연결하면 DAG 상에서 연결됨

    # compile 된 pipeline.yaml 의 dag 파트의 dependency 부분 확인
    # uploaded pipeline 의 그래프 확인
    task_3 = multiply_op(task_1.output, task_2.output)