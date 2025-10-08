import numpy as np
import control as ctrl
from core.imc import IMC
from core.itae import ITAE
from core.znma import ZNMA
from core.chr import CHR, CHR_20

class PIDController:
    def __init__(self):
        self.k = 0
        self.tau = 0
        self.theta = 0
        # vetor de tempo do sistema
        self.tempo = np.array([])
        # sinal de entrada (degrau)
        self.entrada = np.array([])

    def auto_sintonizar(self, method: str, lamb: float = 0):

        if method == 'IMC':
            if lamb < 0.8*self.theta:
                lamb = 0.8*self.theta
            kp = IMC.kp(self.k, self.theta, self.tau, lamb)
            ti = IMC.ti(self.theta, self.tau)
            td = IMC.td(self.theta, self.tau)
        elif method == 'ITAE':
            kp = ITAE.kp(self.k, self.theta, self.tau)
            ti = ITAE.ti(self.theta, self.tau)
            td = ITAE.td(self.theta, self.tau)
        elif method == 'ZNMA':
            kp = ZNMA.kp(self.k, self.theta, self.tau)
            ti = ZNMA.ti(self.theta)
            td = ZNMA.td(self.theta)
        elif method == 'CHR':
            kp = CHR.kp(self.k, self.theta, self.tau)
            ti = CHR.ti(self.tau)
            td = CHR.td(self.theta)
        elif method == 'CHR_20':
            kp = CHR_20.kp(self.k, self.theta, self.tau)
            ti = CHR_20.ti(self.tau)
            td = CHR_20.td(self.theta)
        
        sys = ctrl.tf([self.k], [self.tau, 1])
        [num, den] = ctrl.pade(self.theta, 3)
        sys_pade = ctrl.tf(num, den)
        sys_atraso = ctrl.series(sys, sys_pade)

        pid = ctrl.tf([kp*td, kp, kp/ti], [1, 0])
        cs = ctrl.series(pid, sys_atraso)
        resp = ctrl.feedback(cs)

        sintonia = np.array(ctrl.forced_response(resp, T=self.tempo, U=self.entrada))
        
        steady_value = np.mean(sintonia[1][-int(len(sintonia[1])*0.05):])

        rise_start = np.where(sintonia[1] >= 0.1 * steady_value)[0][0]
        rise_end = np.where(sintonia[1] >= 0.9 * steady_value)[0][0]
        
        tr = self.tempo[rise_end] - self.tempo[rise_start]
        ts = 0
        # Tempo de acomodação (2%)
        low = steady_value * (1 - 0.02)
        high = steady_value * (1 + 0.02)
        for i in range(len(sintonia[1])-1, -1, -1):
            if sintonia[1][i] < low or sintonia[1][i] > high:
                ts = self.tempo[i]
                break
        mp = (np.max(sintonia[1]) - steady_value) / steady_value * 100
        # erro em regime permanente
        ess = self.entrada[-1] - steady_value

        return {
            'sintonia': sintonia,
            'params': [kp, ti, td, lamb],
            'controll_params': [tr, ts, mp, steady_value, ess]
        }
    
    def sintonizar(self, kp, ti, td):
        
        sys = ctrl.tf([self.k], [self.tau, 1])
        [num, den] = ctrl.pade(self.theta, 3)
        sys_pade = ctrl.tf(num, den)
        sys_atraso = ctrl.series(sys, sys_pade)

        pid = ctrl.tf([kp*td, kp, kp/ti], [1, 0])
        cs = ctrl.series(pid, sys_atraso)
        resp = ctrl.feedback(cs)

        sintonia = np.array(ctrl.forced_response(resp, T=self.tempo, U=self.entrada))
        
        steady_value = np.mean(sintonia[1][-int(len(sintonia[1])*0.05):])

        rise_start = np.where(sintonia[1] >= 0.1 * steady_value)[0][0]
        rise_end = np.where(sintonia[1] >= 0.9 * steady_value)[0][0]
        
        tr = self.tempo[rise_end] - self.tempo[rise_start]
        ts = 0
        # Tempo de acomodação (2%)
        low = steady_value * (1 - 0.02)
        high = steady_value * (1 + 0.02)
        for i in range(len(sintonia[1])-1, -1, -1):
            if sintonia[1][i] < low or sintonia[1][i] > high:
                ts = self.tempo[i]
                break
        mp = (np.max(sintonia[1]) - steady_value) / steady_value * 100
        # erro em regime permanente
        ess = self.entrada[-1] - steady_value

        return {
            'sintonia': sintonia,
            'params': [kp, ti, td],
            'controll_params': [tr, ts, mp, steady_value, ess]
        }
    



