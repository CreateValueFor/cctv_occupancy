import numpy as np
import matplotlib.pyplot as plt
import json
from pythermalcomfort.models import pmv_ppd
from pythermalcomfort.utilities import v_relative, clo_dynamic
import random

thermal = []
humid = []

with open("./utils/thermal.json") as file:
    data = json.load(file)
    humid = data['2023-04-12']['humid']
    thermal = data['2023-04-12']['thermal']


def rc_modeling(tn, to, solar,  occupancy, room_c, room_r, time_step, set_temp, threshold, heat_m, cool_m, use_hvac=False, use_occupancy=False):
    temperature = 0

    # RC 네트워크 모델 시뮬레이션
    delta_t = time_step / room_c
    delta_q = (to - tn) / room_r

    # 태양복사량에 따른 열 발생 계산
    solar_heat = solar * 0.8  # 태양복사량에 대한 임의의 계수 곱하기 (임의로 설정)
    delta_q += solar_heat / room_c

    temperature = tn + delta_q * delta_t

    if (use_occupancy == True):
        power_consumption = 50  # 노트북의 평균 전력 소비 (단위: W)
        thermal_efficiency = 0.8  # 노트북의 열 효율 (0.8은 80%를 열로 변환함)
        usage_time = 4  # 노트북의 사용 시간 (단위: 시간)
        heat_generated = power_consumption * \
            thermal_efficiency * usage_time  # 열로 변환된 에너지 (단위: J)

        # 재실 인원에 따른 열 발생 계산
        heat_generation = occupancy * \
            heat_generated  # 사람당 열 발생량 (임의로 설정)
        delta_q += heat_generation / room_c
        temperature = tn + delta_q * delta_t
    hvac_energy = calculate_hvac_needs(temperature, set_temp, threshold,
                                       heat_m, cool_m, room_c, delta_t, delta_q)

    if (use_hvac):

        # HVAC 시스템 제어
        if abs(tn - set_temp) > threshold:
            temperature += hvac_energy / room_c * delta_t
            return [temperature, hvac_energy]
            # heating_power = heat_m
            # cooling_power = 0
            # delta_q += heating_power / room_c
        else:
            heating_power = 0
            cooling_power = 0
            temperature = tn + delta_q * delta_t
            return [temperature, hvac_energy]

        temperature = tn + delta_q * delta_t

        # 목표 온도까지 도달하면 HVAC 시스템 출력을 조절
        if temperature < set_temp:
            heating_power = min(
                heat_m, (set_temp - temperature) * room_c / delta_t)
        elif temperature > set_temp:
            cooling_power = min(
                cool_m, (temperature - set_temp) * room_c / delta_t)

        temperature = temperature + (
            heating_power - cooling_power) * delta_t / room_c
        # temperature[t] += (heating_power - cooling_power) * delta_t / room_capacity

    return [temperature, hvac_energy]


def calculate_hvac_needs(tn, set_temp, threshold, heat_m, cool_m, room_c, delta_t, delta_q):

    if abs(tn - set_temp) > threshold:
        t_diff = abs(tn - set_temp)
        need_delta_q = t_diff / delta_t
        delta_q_diff = abs(delta_q - need_delta_q)
        hvac_power = delta_q_diff * room_c
        return hvac_power
        # heating_power = heat_m
        # cooling_power = 0
        # delta_q += heating_power / room_c
    else:
        return 0

    # HVAC 시스템 제어
    return delta_q_diff


def visualize(time, t, t_o, t_o_h, t_h, y_name):
    # 시뮬레이션 결과 시각화
    plt.plot(time, t, label=f'Room')
    plt.plot(
        time, t_o, label=f'Room occupancy')
    # plt.plot(
    #     time, t_o_h, label=f'Room hvac')
    # plt.plot(
    #     time, t_h, label=f'Room hvac_c')

    plt.xlabel('Time (s)')
    plt.ylabel(y_name)
    plt.legend()
    plt.grid(True)
    plt.show()


def simulate_humidity_change(initial_humidity, notebook_usage_time, number_of_people):
    humidity = initial_humidity
    for _ in range(notebook_usage_time):
        # 노트북 사용으로 인한 습도 변화를 가정합니다.
        # 노트북 사용에 따른 습도 변화 범위 (0.5 ~ 1.5)에 재실 인원 수를 곱합니다.
        humidity_change = random.uniform(0.5, 1.5) * number_of_people
        humidity += humidity_change

        # 습도가 0% 미만이거나 100% 초과로 설정되는 것을 방지합니다.
        humidity = max(0, humidity)
        humidity = min(100, humidity)

    return humidity


def hvac_main():
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
    # 결과 저장을 위한 hvac 변화 추이
    hvac = np.zeros(len(time))
    hvac_occu = np.zeros(len(time))
    hvac_occu_hvac = np.zeros(len(time))
    hvac_occu_hvac_control = np.zeros(len(time))

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
        ori_tdb = temperature[t]
        occu_tdb = temperature_with_occu[t]
        tr = thermal[t]
        rh = humid[t]
        v = 0.1
        met = 1.4
        clo = 0.5

        v_r = v_relative(v=v, met=met)
        clo_d = clo_dynamic(clo=clo, met=met)
        ori_results = pmv_ppd(tdb=ori_tdb, tr=tr, vr=v_r, rh=rh, met=met,
                              clo=clo_d, limit_inputs=False)
        occu_results = pmv_ppd(tdb=occu_tdb, tr=tr, vr=v_r, rh=rh, met=met,
                               clo=clo_d, limit_inputs=False)
        print(ori_results)
        print(occu_results)

        [a, hvac_a] = rc_modeling(temperature[t-1], external_temperature[t],
                                  solar_radiation[t], occupancy[t], room_capacity, room_resistance, time_step, set_temp=23, threshold=1, heat_m=heating_power_max, cool_m=cooling_power_max, use_hvac=False)
        # [a, hvac_a] = rc_modeling(temperature_with_occu[t-1], external_temperature[t],
        #                           solar_radiation[t], occupancy[t], room_capacity, room_resistance, time_step, set_temp=24, threshold=1, heat_m=heating_power_max, cool_m=cooling_power_max, use_hvac=False)
        [b, hvac_b] = rc_modeling(temperature_with_occu[t-1], external_temperature[t],
                                  solar_radiation[t], occupancy[t], room_capacity, room_resistance, time_step, set_temp=24, threshold=1, heat_m=heating_power_max, cool_m=cooling_power_max, use_occupancy=True, use_hvac=False)
        [c, hvac_c] = rc_modeling(temperature_with_occu_hvac[t-1], external_temperature[t],
                                  solar_radiation[t], occupancy[t], room_capacity, room_resistance, time_step, set_temp=24, threshold=1, heat_m=heating_power_max, cool_m=cooling_power_max, use_hvac=True, use_occupancy=True)
        [d, hvac_d] = rc_modeling(temperature_with_occu_hvac_control[t-1], external_temperature[t],
                                  solar_radiation[t], occupancy[t], room_capacity, room_resistance, time_step, set_temp=24, threshold=1, heat_m=heating_power_max, cool_m=cooling_power_max, use_hvac=True, use_occupancy=False)
        temperature[t] = a
        hvac[t] = hvac_a
        temperature_with_occu[t] = b
        hvac_occu[t] = hvac_b
        temperature_with_occu_hvac[t] = c
        hvac_occu_hvac[t] = hvac_c
        temperature_with_occu_hvac_control[t] = d
        hvac_occu_hvac_control[t] = hvac_d

    # print(temperature)
    # print(temperature_with_occu)
    # print(temperature_with_occu_hvac)
    # print(time)
    visualize(time, np.array_split(temperature, 24), np.array_split(temperature_with_occu, 24),
              np.array_split(temperature_with_occu_hvac, 24), np.array_split(temperature_with_occu_hvac_control, 24), y_name='Temperature (°C)')
    visualize(time, np.array_split(temperature - 24, 24), np.array_split(temperature_with_occu - 24, 24),
              np.array_split(temperature_with_occu_hvac, 24), np.array_split(temperature_with_occu_hvac_control, 24), y_name='Temperature (°C)')

    visualize(time, np.array_split(hvac, 24), np.array_split(hvac_occu, 24),
              np.array_split(hvac_occu_hvac, 24), np.array_split(hvac_occu_hvac_control, 24), y_name="Hvac Heat/Cool Power (W)")
    print(np.sum(hvac))
    print(np.sum(hvac_occu))
    return
    return [temperature, hvac, temperature_with_occu, hvac_occu]
