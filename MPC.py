from pickle import FALSE
import time
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import mpcUtil as u
import matplotlib.dates as mdates
import pandas as pd

# x = [0]
# y = [23]
# result = 0

# fig, ax = plt.subplots()
# ax.set_xlim(0, 100)
# ax.set_ylim(18, 28)


def animate(i, x, y):
    y_data = result

    x.append(x[-1] + 1)
    y.append(y_data)

    x = x[-100:]  # 최근 100개만 봄
    y = y[-100:]

    ax.clear()
    ax.plot(x, y)


# [dfTime, dfOccupancy, time, occupancy_list] = u.get_occupancy(
#     './logs/20230420.csv')
[dfTime, dfOccupancy, time, occupancy_list] = u.get_occupancy(
    './sorted.csv')

solutions = []

for occupancy in occupancy_list:
    # 실시간으로 환경 변수(실내 온도, 습도, 재실 인원 수 등)를 감지
    ti = u.get_indoor_temperature()
    # continue
    # 최적화 알고리즘을 이용하여 최적의 제어 입력 구하기
    x0 = [20, 25, 5, occupancy]
    bnd = ((18, 25), (22, 28), (0, 10), (0, 20))
    con1 = {'type': 'ineq', 'fun': u.constraint1}
    con2 = {'type': 'ineq', 'fun': u.constraint2}
    con3 = {'type': 'ineq', 'fun': u.constraint3}
    con4 = {'type': 'ineq', 'fun': u.constraint4}
    cons = [con1, con2, con3, con4]
    solution = minimize(u.objective, x0, method='SLSQP',
                        bounds=bnd, constraints=cons)
    result = u.control(solution.x)
    solutions.append(result)

    # 제어기를 이용하여 에어컨의 설정 온도 변경하기
    # print(result)

    # animation = FuncAnimation(fig, animate, fargs=(x, y), frames=[])

    # time.sleep(1)  # 1초마다 반복
fig, ax = plt.subplots()
dfSolutions = pd.DataFrame({'Occupancy': solutions})
ax.plot(dfTime, dfSolutions)

# x 축 눈금 설정
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.title("MPC Results")
plt.show()
plt.close()
