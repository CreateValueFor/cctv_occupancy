# 𝑉𝑁(𝑒0, 𝑈, 𝑉) := 12⎡⎣⎢(𝑥𝑁−𝑥𝑟)𝑇𝑃(𝑥𝑁−𝑥𝑟) +∑𝑘 = 1𝑁−1𝑒𝑇𝑘𝑄𝑒𝑘 +∑𝑘 = 0𝑁−1𝑢𝑘𝑇𝑅𝑢𝑘⎤⎦⎥,
import numpy as np
import math


# def calculate_pmv(x, T_i, T_o, H_r):
#     """
#     인자:
#     x : np.array([M, W, Cl, Ta]) - 인간 대사율, 옷의 저항성, 옷의 열 전달 계수, 실내온도
#     T_i : float - 실내 온도
#     T_o : float - 실외 온도
#     H_r : float - 상대 습도

#     반환값:
#     float - PMV
#     """
#     M, W, Cl, Ta = x
#     I_cl = 2.38 * 10**(-3) * Cl * (T_i - Ta)
#     W_m = W / 60
#     M_w = M - W_m
#     F_cl = 1.05 + 0.645 * Cl
#     E_R = 0.42 * (M - 58.15)
#     E_D = 3.05 * 10**(-3) * (5733 - 6.99 * (M - 273) - H_r *
#                              (0.1333 + 0.0027 * (M - 273))) * W_m
#     E_L = 0.017 * M * (5867 - H_r * (0.275 - 0.0018 * M) - Ta)
#     PMV = 0.303 * np.exp(-0.036 * M) + 0.028 * (T_i - T_o) + \
#         F_cl * (E_R + E_D + E_L) - 3.05
#     return abs(PMV)

def calculate_pmv(ta, tr, rh, met, clo):
    """
    PMV 계산을 위한 함수

    매개변수:
    ta (float): 공기 온도 (°C)
    tr (float): 평균 반대편면 온도 (°C)
    rh (float): 상대 습도 (%)
    met (float): 활동 대사율 (met)
    clo (float): 옷의 저항성 (clo)

    반환값:
    pmv (float): 계산된 PMV 값
    """

    # 상수 정의
    pa = rh * 10 * math.exp(16.6536 - 4030.183 / (ta + 235))  # 수증기 압력 (Pa)
    icl = 0.155 * clo  # 표면 옷의 표면적 지수
    m = met * 58.15  # 활동 대사율 (W/m²)

    # PMV 계산
    pmv = (0.303 * math.exp(-0.036 * m) + 0.028) * (m - 3.05) \
        + (0.42 * math.exp(-0.04 * m) + 0.078) * (icl - 0.155) \
        + 3.96 * 10**-8 * icl * (34 - ta) \
        + 0.303 * math.exp(-0.036 * m) * (5.867 - 0.82 * (pa / icl)) \
        + 0.132 * icl * (tr - ta)

    return pmv
