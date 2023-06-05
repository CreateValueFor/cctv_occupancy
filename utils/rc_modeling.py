import numpy as np

# constants
# C1 = 9.356 * (10 ** 5)  # kJ/C
C1 = 9.356e5  # kJ/C
# C2 = 2.970 * (10 ** 6)  # kJ/C
C2 = 2.970e6
# CW = 6.695 * (10 ** 5)  # kJ/C
CW = 6.695e5
K1 = 16.48  # kJ/C
# K2 = 108.5  # kJ/C
K2 = 108.5  # kJ/C
K3 = 5  # kJ/C
K4 = 30.5  # kJ/C
K5 = 23.04  # kJ/C

Ac = np.array([
    [-(K1+K2+K3+K5)/C1, (K1 + K2)/C1, K5/C1],
    [(K1+K2)/C2, -(K1+K2)/C2, 0],
    [K5/CW, 0, -(K4+K5)/CW]
])

Bc = np.array([
    [1/C1, 1/C1],
    [0, 0],
    [0, 0]
])

Cc = np.array([
    [K3/C1, 1/C1, 1/C1],
    [0, 1/C2, 0],
    [K4/CW, 0, 0]
])

# # variables
# x1 : indoor air termperature
# x2 : interior wall temperature
# x3 : exterior-wall core temperature
# u1 : cooling power
# u2 : heating power
# lm1 : ambient temperature
# lm2 : solar radiation
# lm3 : internal heat gain


def getNextSystemValue(Xc, Uc, Lc):
    # print(np.dot(Ac, Xc) * 10e3)
    # print(np.dot(Bc, Uc) * 10e4)
    # print(np.dot(Cc, Lc) * 10e3)
    Xk = np.dot(Ac, Xc) + \
        np.dot(Bc, Uc) + \
        np.dot(Cc, Lc) * 10e3
    # print(Xk)
    # np.array([[15, 15, 15]]).T

    return Xk


def getNextSystemValue2(Xc, Uc, Lc):
    X1 = (
        (K1+K2)*(Xc[1]-Xc[0]) + K5*(Xc[2]-Xc[0]) +
        K3*(Lc[0] - Xc[0]) +
        Uc[0] +
        Uc[1] +
        Lc[1] +
        Lc[2]
    )/C1

    X2 = ((K1+K2) * (Xc[0] - Xc[1]) + Lc[1])/C2

    X3 = (K5*(Xc[0] - Xc[2]) + K4*(Lc[0]-Xc[2]))/CW
    return np.array([[X1, X2, X3]])
