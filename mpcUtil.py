import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import minimize


def objective(x):
    # print(x)
    # 목적 함수: 실내 온도와 설정 온도의 차이를 최소화

    return (x[0] - x[1])**2


def constraint1(x):
    # 제약 조건 1: 제어 입력이 최소값과 최대값 범위 내에 있어야 함
    return x[0] - 18


def constraint2(x):
    # 제약 조건 2: 제어 입력 변화율이 최대값 범위 내에 있어야 함
    return x[0] - x[2]


def constraint3(x):
    # 제약 조건 3: 실내 온도가 최소값과 최대값 범위 내에 있어야 함
    return x[1] - 22


def constraint4(x):
    # 제약 조건 4: 재실 인원 수가 최대값 범위 내에 있어야 함
    return x[3] - 20


def control(x):
    # 제어 입력에 따라 에어컨의 설정 온도를 변경하는 함수
    return x[0]


def get_indoor_temperature():
    return 22


def get_occupancy(csv):
    df = pd.read_csv(csv)

    df = df[(df['Time'].str.len() == 20)]

    # return
    df['Time'] = pd.to_datetime(df['Time'], format='%Y%m%d %H:%M:%S:%f')
    # plot 그리기
    fig, ax = plt.subplots()
    ax.plot(df['Time'], df['Occupancy'])
    plt.title("Occupancy flow")

    # x 축 눈금 설정
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # 그래프 출력
    # plt.show()
    # print(df['Occupancy'].values.tolist())
    return [df['Time'], df['Occupancy'], df['Time'].values.tolist(), df['Occupancy'].values.tolist()]
