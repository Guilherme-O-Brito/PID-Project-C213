# método CHR sem overshoot
class CHR:

    @staticmethod
    def kp(k, theta, tau):
        return ((0.6*tau)/(k*theta))
    
    @staticmethod
    def ti(tau):
        return (tau)
    
    @staticmethod
    def td(theta):
        return (theta/2)

# método CHR 20% de overshoot
class CHR_20:

    @staticmethod
    def kp(k, theta, tau):
        return ((0.95*tau)/(k*theta))
    
    @staticmethod
    def ti(tau):
        return (1.357*tau)
    
    @staticmethod
    def td(theta):
        return (0.473*theta)