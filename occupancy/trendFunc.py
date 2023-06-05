import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd

result = pd.read_csv('sorted.csv')

result['Date'] = result['Time'].str[:10]
result['Hour'] = result['Time'].str[11:]

# 그룹화된 데이터를 저장할 딕셔너리 생성
daily_totals = result.groupby('Date')['Occupancy'].sum().reset_index()

print(daily_totals)
# 추세선 함수로 사용할 함수 정의 (예시: 1차 다항식)


def trend_func(x, a, b):
    return a * x + b


# x 값은 1부터 시작하는 일자로 설정
x = np.arange(1, len(daily_totals) + 1)

# 추세선 적합
params, _ = np.polyfit(x, daily_totals['Occupancy'], 1)

# 추세선 예측
predicted_totals = trend_func(x, params[0], params[1])

# 결과 출력
print("추세선 함수 파라미터:", params)

# 그래프 그리기
plt.plot(x, daily_totals['Occupancy'], 'bo',
         label='일별 재실 인원 수')  # 일별 재실 인원 데이터
plt.plot(x, predicted_totals, 'r-', label='추세선')  # 추세선
plt.xlabel('일자')
plt.ylabel('재실 인원 수')
plt.legend()
plt.show()
