# método Cohen e Coon sem overshoot
class CeC:

    @staticmethod
    def kp(k, theta, tau):
        return ((tau/(k*theta))*(((16*tau)+(3*theta))/(12*tau)))
    
    @staticmethod
    def ti(theta, tau):
        return (theta*((32+((6*theta)/tau))/(13+((8*theta)/tau))))
    
    @staticmethod
    def td(theta, tau):
        return ((4*theta)/(11+((2*theta)/tau)))