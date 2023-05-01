import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import minimize
from scipy.optimize import Bounds


def get_proportional_constant(rho):
    return 1


def calculate_pmv(x, T_i, T_o, H_r):
    """
    인자:
    x : np.array([M, W, Cl, Ta]) - 인간 대사율, 옷의 저항성, 옷의 열 전달 계수, 실내온도
    T_i : float - 실내 온도
    T_o : float - 실외 온도
    H_r : float - 상대 습도

    반환값:
    float - PMV
    """
    M, W, Cl, Ta = x
    I_cl = 2.38 * 10**(-3) * Cl * (T_i - Ta)
    W_m = W / 60
    M_w = M - W_m
    F_cl = 1.05 + 0.645 * Cl
    E_R = 0.42 * (M - 58.15)
    E_D = 3.05 * 10**(-3) * (5733 - 6.99 * (M - 273) - H_r *
                             (0.1333 + 0.0027 * (M - 273))) * W_m
    E_L = 0.017 * M * (5867 - H_r * (0.275 - 0.0018 * M) - Ta)
    PMV = 0.303 * np.exp(-0.036 * M) + 0.028 * (T_i - T_o) + \
        F_cl * (E_R + E_D + E_L) - 3.05
    return abs(PMV)


# 목적 함수
def objective(x, T_i, T_o, H_r, T_goal, rho):
    """
    인자:
    x : np.array([M, W, Cl, Ta]) - 인간 대사율, 옷의 저항성, 옷의 열 전달 계수, 실내온도
    T_i : float - 실내 온도
    T_o : float - 실외 온도
    H_r : float - 상대 습도
    T_goal : float - 목표 온도
    rho : float - 재실밀도

    반환값:
    float - (PMV - k * T_i)**2
    """
    PMV = calculate_pmv(x, T_i, T_o, H_r)
    k = get_proportional_constant(rho)
    return (PMV - k * T_i - T_goal)**2

# 제약조건 설정 함수


def get_constraint(T_i_min, T_i_max):
    """
    인자:
    T_i_min : float - 실내 온도 하한값
    T_i_max : float - 실내 온도 상한값

    반환값:
    object - Scipy.optimize.Bounds() 객체
    """
    bounds = Bounds(T_i_min, T_i_max)
    return bounds

# MPC 구현 함수


def mpc(T_i, T_o, H_r, T_goal, rho, T_i_min, T_i_max):
    """
    인자:
    T_i : np.array - 실내 온도 시계열
    T_o : np.array - 실외 온도 시계열
    H_r : np.array - 상대 습도 시계열
    T_goal : np.array - 목표 온도 시계열
    rho : np.array - 재실밀도 시계열
    T_i_min : float - 실내 온도 하한값
    T_i_max : float - 실내 온도 상한값

    반환값:
    np.array - 최적화된 실내 온도 시계열
    """
    n_steps = len(T_i)  # 시계열 길이
    x0 = np.array([1.0, 0.5, 0.5, T_i[0]])  # 초기값
    res = minimize(objective,
                   x0,
                   args=(T_i[0], T_o[0], H_r[0], T_i[0],
                         rho[0], T_i_min, T_i_max),
                   method='SLSQP',
                   bounds=get_constraint(T_i_min, T_i_max)
                   )  # 최적화
    T_i_opt = np.zeros(n_steps)
    T_i_opt[0] = res.x[-1]  # 최적화된 초기값
    for t in range(1, n_steps):
        x0 = res.x  # 이전 최적값으로 초기값 설정
        res = minimize(objective, x0, args=(T_i_opt[t-1], T_o[t], H_r[t], T_goal[t], rho[t],
                       T_i_min, T_i_max), method='SLSQP', bounds=get_constraint(T_i_min, T_i_max))  # 최적화
        T_i_opt[t] = res.x[-1]  # 최적화된 결과 저장
    return T_i_opt
