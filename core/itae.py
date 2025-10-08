class ITAE:
    A = 0.965
    B = -0.85
    C = 0.796
    D = -0.147
    E = 0.308
    F = 0.929

    @staticmethod
    def kp(k, theta, tau):
        return ((ITAE.A/k)*((theta/tau)**(ITAE.B)))
    
    @staticmethod
    def ti(theta, tau):
        return ((tau)/((ITAE.C+ITAE.D)*(theta/tau)))
    
    @staticmethod
    def td(theta, tau):
        return (tau*ITAE.E*(theta/tau)**ITAE.F)