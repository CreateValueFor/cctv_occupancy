import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import csv
from scipy.optimize import minimize
from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter


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


def agfregate_csv(path):
    result = pd.DataFrame()
    # print(path)
    file_list = os.listdir(path)
    # print(file_list)

    for file in file_list:
        # df = pd.read_csv(path+file, quoting=csv.QUOTE_NONE,
        #                  sep=", ,", engine='python')
        df = pd.read_csv(path+file, quoting=csv.QUOTE_NONE)
        # print(len(df))
        nan = df.dropna()
        # print(len(df))
        # print(len(nan))
        new_result = pd.DataFrame()
        if len(nan) == 0:
            for i in range(0, len(df), 2):
                if (i+1 >= len(df)):
                    break
                time_col = df.iloc[i]['Time']
                occupancy_col = df.iloc[i+1]['Occupancy']

                new_df = pd.DataFrame(
                    {'Time': [time_col], 'Occupancy': [occupancy_col]})
                new_result = pd.concat([new_result, new_df])
            result = pd.concat([result, new_result])
        else:
            result = pd.concat([result, df])
        # temp_df = pd.DataFrame(result.iloc[i:i+2].values.flatten()).T
        # new_col = pd.concat([new_col, temp_df], axis=0, ignore_index=True)
        # result = pd.concat([result, df])
        # print(len(new_result))
    print(result)
    print(result.dropna())

    clean_data = result.dropna()
    clean_data['Time'] = pd.to_datetime(clean_data['Time'], errors='coerce')
    valid_df = clean_data[(clean_data['Time'].dt.strftime(
        '%Y-%m-%d %H:%M:%S') != 'NaT') | (clean_data['Time'].dt.strftime('%Y-%m-%d %H:%M') != 'NaT')]
    valid_df = valid_df.dropna(subset=['Time'])

    print(len(valid_df))

    sorted_df = valid_df.sort_values(by="Time")
    print(sorted_df)
    # sorted_df.to_csv('sorted.csv', index=False)

    # 시각화
    plt.plot(sorted_df['Time'], sorted_df['Occupancy'])
    plt.xlabel('Time')
    plt.ylabel('Occupancy')
    plt.title('Occupancy over Time')
    # plt.show()

    # 2023년 5월 4일치 데이터 시각화
    mask = (sorted_df['Time'].dt.year == 2023) & (
        sorted_df['Time'].dt.month == 4) & (sorted_df['Time'].dt.day == 5)
    df_filtered = sorted_df.loc[mask]
    df_filtered['Time'] = df_filtered['Time'].dt.strftime('%H:%M')

    fig, ax = plt.subplots()

    ax.set_xticks(df_filtered.index)
    ax.xaxis.set_major_locator(plt.MultipleLocator(60))  # 10분 간격
    ax.set_xlabel('Time')

    ax.plot(df_filtered['Time'], df_filtered['Occupancy'])

    #  2023년 5월 5일치 데이터 시각화
    mask = (sorted_df['Time'].dt.year == 2023) & (
        sorted_df['Time'].dt.month == 4) & (sorted_df['Time'].dt.day == 6)
    df_filtered = sorted_df.loc[mask]
    df_filtered['Time'] = df_filtered['Time'].dt.strftime('%H:%M')

    fig, ax = plt.subplots()

    ax.set_xticks(df_filtered.index)
    ax.xaxis.set_major_locator(plt.MultipleLocator(60))  # 10분 간격
    ax.set_xlabel('Time')

    ax.plot(df_filtered['Time'], df_filtered['Occupancy'])

    plt.show()

    return result


def show_trends(path):
    result = pd.read_csv(path)
    result['Date'] = result['Time'].str[:10]
    result['Hour'] = result['Time'].str[11:]
    grouped = result.groupby('Date')

    # 그룹화된 데이터를 저장할 딕셔너리 생성
    grouped_data = {}
    groups_to_plot = []

    for group, group_data in grouped:
        grouped_data[group] = group_data
        groups_to_plot.append(group)

    # 그래프 그리기
    for group, group_data in grouped_data.items():
        if group == '2023-04-09':
            continue
        x_values = pd.to_datetime(group_data['Hour'])
        plt.plot(x_values, group_data['Occupancy'], label=group)

    # x 축 간격을 30분 단위로 설정
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(byminute=range(0, 60, 60)))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # 그래프 축 및 레이블 설정
    plt.xlabel('Hour')
    plt.ylabel('Occupancy')
    plt.title('Occupancy by Date')
    plt.legend()

    # # 그래프 보여주기
    plt.show()
