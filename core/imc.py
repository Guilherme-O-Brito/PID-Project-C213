class IMC:

    @staticmethod
    def kp(k, theta, tau, lamb):
        return ((2*tau+theta)/(k*(2*lamb+theta)))
    
    @staticmethod
    def ti(theta, tau):
        return (tau*(theta/2))
    
    @staticmethod
    def td(theta, tau):
        return ((tau*theta)/(2*tau+theta))
    
    @staticmethod
    def cd(theta, lamb):
        return True if (lamb/theta) > 0.8 else False