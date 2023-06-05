import numpy as np
from utils.cost_function import calculate_pmv
from utils.rc_modeling import getNextSystemValue
import json
from pythermalcomfort.models import pmv_ppd
from pythermalcomfort.utilities import v_relative, clo_dynamic

from utils.rc_modeling2 import hvac_main, rc_modeling

X0 = np.array([[20, 18, 12]]).T
U0 = np.array([[0, 0]]).T


x = [X0]

thermal = []
humid = []

with open("thermal.json") as file:
    data = json.load(file)
    humid = data['2023-04-12']['humid']
    thermal = data['2023-04-12']['thermal']


# print(results)
# print(x)


def __main__():
    # 구획 정보 설정
    room_capacity = 14400  # 구획 열용량 (J/°C)
    room_resistance = 10  # 구획 열저항 (°C/W)

    # 외부 조건 설정
    external_temperature = np.array(thermal)  # 외기온도 (°C)

    # 태양
    base_value = 2000
    lower_limit = 100
    upper_limit = 200
    array_length = 24

    random_array = np.random.randint(
        lower_limit, upper_limit + 1, size=array_length)
    result_array = base_value + random_array
    solar_radiation = result_array  # 태양복사량 (W/m^2)

    # 초기 조건 설정
    initial_temperature = 20  # 초기 온도 (°C)

    # 시뮬레이션 파라미터 설정
    simulation_duration = 24 * 60 * 60  # 시뮬레이션 기간 (초)
    time_step = 60 * 60  # 시간 단계 (초)

    # 재실 인원 모델링
    time = np.arange(0, simulation_duration, time_step)
    occupancy = np.random.randint(
        low=40, high=100, size=len(time))  # 재실 인원 수 (임의로 생성)

    # 결과 저장을 위한 배열 초기화
    temperature = np.zeros(len(time))
    temperature_with_occu = np.zeros(len(time))
    temperature_with_occu_hvac = np.zeros(len(time))
    temperature_with_occu_hvac_control = np.zeros(len(time))

    # HVAC 시스템 제어 변수 설정
    heating_power_max = 100000 * 10  # 난방 시스템 출력 (W)
    cooling_power_max = 100000 * 10  # 냉방 시스템 출력 (W)

    # 시뮬레이션 파라미터 설정
    simulation_duration = 24 * 60 * 60  # 시뮬레이션 기간 (초)
    time_step = 60 * 60  # 시간 단계 (초)

    temperature[0] = initial_temperature
    temperature_with_occu[0] = initial_temperature
    temperature_with_occu_hvac[0] = initial_temperature
    temperature_with_occu_hvac_control[0] = initial_temperature

    for t in range(1, len(time)):
        [a, b, c, d] = rc_modeling(temperature_with_occu_hvac_control[t-1], external_temperature[t],
                                   solar_radiation[t], occupancy[t], room_capacity, room_resistance, time_step, set_temp=23, threshold=1, heat_m=heating_power_max, cool_m=cooling_power_max)
        temperature[t] = a
        temperature_with_occu[t] = b
        temperature_with_occu_hvac[t] = c
        temperature_with_occu_hvac_control[t] = d

    for i in range(0, 24):
        lm0 = np.array([[thermal[i], 2.05, 2]]).T

        x.append(x[i] - getNextSystemValue(x[i], U0, lm0))
        print(getNextSystemValue(x[i], U0, lm0))
        # print(x)

        p = np.array([65, 0.75, 3, thermal[i]])
        # tdb = x[i][0]
        # tdb = thermal[i]
        tdb = temperature[i]
        # tr = 25
        # tr = x[i][0]
        # tr = thermal[i]
        tr = temperature[i]
        rh = humid[i]
        v = 0.1
        met = 1.4
        clo = 0.5

    # pmv = calculate_pmv(x[i][0], thermal[i], humid[i], met, clo)

        v_r = v_relative(v=v, met=met)
        clo_d = clo_dynamic(clo=clo, met=met)
        results = pmv_ppd(tdb=tdb, tr=tr, vr=v_r, rh=rh, met=met,
                          clo=clo_d, limit_inputs=False)
        print(results)


hvac_main()
