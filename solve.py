import scipy as sci
import numpy as np

from paintshit import paintshit


class Body:
    def __init__(self, m: float, rx: float, ry: float, rz: float, vx: float, vy: float, vz: float):
        self.m = m
        self.r = np.array([rx, ry, rz])
        self.v = np.array([vx, vy, vz])
def solve(bodies: list[Body]):
    G = 6.67408e-11
    m_nd = 1.989e+30  # kg
    r_nd = 5.326e+12  # m
    v_nd = 30000  # m/s
    t_nd = 79.91 * 365.25 * 24 * 3600  # s
    K1 = G * t_nd * m_nd / (r_nd ** 2 * v_nd)
    K2 = v_nd * t_nd / r_nd

    def FourBodyEquations(w, t, ms_):
        rs_ = []
        vs_ = []
        for j in range(0, len(w)//2, 3):
            rs_.append(w[j:j+3])
        for j in range(len(w)//2, len(w), 3):
            vs_.append(w[j:j+3])
        r_ = [[0.0]*(len(bodies)) for _ in range(len(bodies))]
        for i_ in range(len(bodies)):
            for j_ in range(i_+1, len(bodies)):
                r_[i_][j_] = sci.linalg.norm(rs_[j_]-rs_[i_])
                r_[j_][i_] = sci.linalg.norm(rs_[j_]-rs_[i_])

        dvsbydt = []
        drsbydt = []
        for j_ in range(len(bodies)):
            su = 0
            for n_ in range(len(bodies)):
                if j_ == n_: continue
                su += K1 * ms_[n_] * (rs_[n_] - rs_[j_]) / r_[n_][j_] ** 3
            dvsbydt.append(su)
        for j_ in range(len(bodies)):
            drsbydt.append(K2*vs_[j_])

        r_derivs = np.concatenate((drsbydt[0], drsbydt[1]))
        v_derivs = np.concatenate((dvsbydt[0], dvsbydt[1]))
        for j_ in range(2, len(bodies)):
            r_derivs = np.concatenate((r_derivs, drsbydt[j_]))
            v_derivs = np.concatenate((v_derivs, dvsbydt[j_]))
        derivs = np.concatenate((r_derivs, v_derivs))
        return derivs
    rs = []
    vs = []
    ms = []
    for body in bodies:
        rs.append(body.r)
        vs.append(body.v)
        ms.append(body.m)
    init_params = np.array(rs+vs)  # Package initial parameters into one size-24 array
    init_params = init_params.flatten()  # Flatten the array to make it 1D
    time_span = np.linspace(0, 20, 1000)  # Time span is 20 orbital years and 1000 points

    import scipy.integrate
    three_body_sol = sci.integrate.odeint(FourBodyEquations, init_params, time_span, args=(ms, ))

    res = []
    for jj in range(0, len(bodies)*3, 3):
        res.append(three_body_sol[:, jj:jj+3])
    return res
paintshit(*solve([
    Body(1.1, *[-0.5, 1, 0], *[0.02, 0.02, 0.02]),
    Body(5.907, *[5.5, 4, 0.5], *[-1, 0, -0.1]),
    Body(1.425, *[0.2, 1, 1.5], *[0, -0.03, 0]),
    Body(2.425, *[0, 0, 0], *[0, 0, 0])
]))