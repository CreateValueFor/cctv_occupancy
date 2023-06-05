import numpy as np
from scipy.optimize import minimize


# 목적 함수 정의


def objective_function(x, room_c, initial_state, horizon, set_temp, delta_t):
    # x: HVAC 시스템 출력 (0~100)
    state = initial_state  # 초기 상태
    total_energy = 0.0  # 총 에너지 소비량

    for _ in range(horizon):
        # 현재 상태와 출력으로 다음 상태 예측
        next_state = state + (x/room_c * delta_t)  # 예측된 다음 상태

        # 목적 함수: 목표 온도와의 오차 제곱의 합 최소화
        objective = (next_state - set_temp) ** 2

        # 총 에너지 소비량 계산
        total_energy += x * delta_t

        # 상태 업데이트
        state = next_state

    return objective + total_energy


def MPC():
    # MPC 알고리즘 파라미터 설정
    horizon = 24  # MPC의 예측 단계 수
    dt = 1  # 시간 단계 (시간당 1시간)

    # 초기 상태 및 목표 온도 설정
    initial_state = 20.0  # 초기 실내 온도
    target_temperature = 23.0  # 목표 실내 온도

    # HVAC 시스템 제어 변수 설정
    min_output = 0.0  # 최소 출력
    max_output = 100000.0  # 최대 출력
    # 제약 조건
    constraints = ({'type': 'ineq', 'fun': lambda x: x - min_output},
                   {'type': 'ineq', 'fun': lambda x: max_output - x})

    # 초기 추정치
    initial_guess = np.zeros(horizon)

    # 최적화 수행
    result = minimize(objective_function, initial_guess,
                      constraints=constraints)

    # 결과 출력
    optimal_output = result.x
    total_energy_consumption = result.fun

    print("Optimal HVAC Output:", optimal_output)
    print("Total Energy Consumption:", total_energy_consumption)
