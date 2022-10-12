import math
import numpy as np
import numba

def LeibnizFormula1(nmax):
    s = 0
    for i in range(0,nmax+1):
        a = (-1)**i * 1/(2*i + 1)
        s += a
    return 4*s

def LeibnizFormula2(nmax):
    s = np.array([(-1)**i * 1/(2*i + 1) for i in range(0,nmax+1)])
    return 4*np.sum(s)

def LeibnizFormula3(nmax):
    s = np.sum([(-1)**i * 1/(2*i + 1) for i in range(0,nmax + 1)])
    return 4*s

@numba.jit
def LeibnizFormula4(nmax):
    s = 0
    for i in range(nmax+1):
        s += (-1)**i * 1/(2*i + 1)
    return 4*s



if __name__ == "__main__":
    import sys
    f = eval(sys.argv[1])
    pi = f(10**8)
    print(pi)
