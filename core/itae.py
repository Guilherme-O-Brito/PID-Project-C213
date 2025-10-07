class ITAE:
    @staticmethod
    def kp(k, theta, tau):
        return ((0.965/k)*((theta/tau)**(-0.85)))
    
    @staticmethod
    def ti(k, theta, tau):
        return ((tau)/(0.796-0.147*(theta/tau)))
    
    @staticmethod
    def td(theta, tau):
        return (tau*0.308*(theta/tau)**0.929)