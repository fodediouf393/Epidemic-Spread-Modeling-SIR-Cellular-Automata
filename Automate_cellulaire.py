import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as alg
import numpy.random as nrd
import random as rd

def grid(n):
    M = []
    for i in range(n):
        L = []
        for j in range(n):
            L.append(0)
        M.append(L)
    return M

def point(n, p):
    M = grid(n)
    for k in range(p):
        i, j = rd.randrange(n), rd.randrange(n)
        while M[i][j] == 1:
            i, j = rd.randrange(n), rd.randrange(n)
        M[i][j] = 1
    return M

def Exposed(M, i, j):
    n = len(M)
    if i == 0 and j == 0:
        return (M[0][1]-1)*(M[1][1]-1)*(M[1][0]-1) == 0
    elif i == 0 and j == n-1:
        return (M[0][n-2]-1)*(M[1][n-2]-1)*(M[1][n-1]-1) == 0
    elif i == n-1 and j == 0:
        return (M[n-1][1]-1)*(M[n-2][1]-1)*(M[n-2][0]-1) == 0
    elif i == n-1 and j == n-1:
        return (M[n-1][n-2]-1)*(M[n-2][n-2]-1)*(M[n-2][n-1]-1) == 0
    elif i == 0:
        return (M[0][j-1]-1)*(M[1][j-1]-1)*(M[1][j]-1)*(M[1][j+1]-1)*(M[0][j+1]-1) == 0
    elif i == n-1:
        return (M[n-1][j-1]-1)*(M[n-2][j-1]-1)*(M[n-2][j]-1)*(M[n-2][j+1]-1)*(M[n-1][j+1]-1) == 0
    elif j == 0:
        return (M[i-1][0]-1)*(M[i-1][1]-1)*(M[i][1]-1)*(M[i+1][1]-1)*(M[i+1][0]-1) == 0
    elif j == n-1:
        return (M[i-1][n-1]-1)*(M[i-1][n-2]-1)*(M[i][n-2]-1)*(M[i+1][n-2]-1)*(M[i+1][n-1]-1) == 0
    else:
        return (M[i-1][j-1]-1)*(M[i-1][j]-1)*(M[i-1][j+1]-1)*(M[i][j-1]-1)*(M[i][j+1]-1)*(M[i+1][j-1]-1)*(M[i+1][j]-1)*(M[i+1][j+1]-1) == 0

def bernoulli(p):
    return nrd.binomial(1, p)

def transition(M, p1, p2):
    n = len(M)
    nouv = grid(n)
    for i in range(n):
        for j in range(n):
            if M[i][j] > 1:
                nouv[i][j] = M[i][j]
            elif M[i][j] == 1:
                if bernoulli(p1) == 1:
                    nouv[i][j] = 3
                else:
                    nouv[i][j] = 2
            else:
                if Exposed(M, i, j):
                    if bernoulli(p2) == 1:
                        nouv[i][j] = 1
    return nouv

def count(M):
    S = I = R = D = 0
    for i in range(len(M)):
        for j in range(len(M[i])):
            if M[i][j] == 0:
                S += 1
            elif M[i][j] == 1:
                I += 1
            elif M[i][j] == 2:
                R += 1
            elif M[i][j] == 3:
                D += 1
    return [S, I, R, D]

def SIR(n, p, p1, p2):
    M = point(n, p)
    nb = count(M)
    temps = 0
    S = [nb[0]]
    I = [nb[1]]
    R = [nb[2]]
    D = [nb[3]]
    while nb[1] > 0:
        M = transition(M, p1, p2)
        nb = count(M)
        S.append(nb[0])
        I.append(nb[1])
        R.append(nb[2])
        D.append(nb[3])
    T = np.linspace(0, len(S)-1, len(S))
    plt.plot(T, S, color='g', label='Sains')
    plt.plot(T, I, color='r', label='Infectés')
    plt.plot(T, R, color='b', label='Rétablis')
    plt.plot(T, D, color='k', label='Décédés')
    plt.legend()
    return plt.show()
