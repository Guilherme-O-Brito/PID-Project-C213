# método de Ziegler-Nichols Malha Aberta - ZNMA
class ZNMA:

    @staticmethod
    def kp(k, theta, tau):
        return ((1.2*tau)/(k*theta))
    
    @staticmethod
    def ti(theta):
        return (2*theta)
    
    @staticmethod
    def td(theta):
        return (theta/2)