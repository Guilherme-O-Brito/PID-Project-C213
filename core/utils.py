from scipy.io import loadmat
import numpy as np

def import_dataset(path:str) -> dict:
    # Importando o dataset com o caminho dado
    dataset = loadmat(path)
    
    # Separando os dados lidos em arrays do numpy 
    dados_entrada = np.array(dataset['dados_entrada'])
    dados_saida = np.array(dataset['dados_saida'])
    tempo = np.array(dataset['tiempo'])[0, :]
    entrada = np.array(dataset['entrada'])[0, :]
    saida = np.array(dataset['salida'])[0, :]
    parametros = dataset['parametros_sistema']

    return {
        'dados_entrada': dados_entrada,
        'dados_saida': dados_saida,
        'tempo': tempo,
        'entrada': entrada,
        'saida': saida,
        'parametros': parametros
    }

class IMC:
    def __init__(self,tau:float,teta:float,lamb:float,k:float):
        self.tau = tau
        self.teta = teta
        self.lamb = lamb
        self.k = k
        self.kp = self.Kp()
        self.ti = self.Ti()
        self.td = self.Td()
        self.cd = self.CD()

    def Kp(self):
        return((2*self.tau+self.teta)/(self.k*(2*self.lamb+self.teta)))
    
    def Ti(self):
        return(self.tau(self.teta/2))
    
    def Td(self):
        return((self.tau*self.teta)/(2*self.tau+self.teta))
    
    def CD(self):
        return True if (self.lamb/self.teta) > 0.8 else False
    

class ITAE:
    def __init__(self,tau:float,teta:float,k:float):
        self.tau = tau
        self.teta = teta
        self.k = k
        self.kp = self.Kp()
        self.ti = self.Ti()
        self.td = self.Td()
    
    def Kp(self):
        return ((0.965/self.k)*((self.teta/self.tau)**(-0.85)))
    
    def Ti(self):
        return ((self.tau)/(0.796-0.147*(self.teta/self.tau)))
    
    def Td(self):
        return (self.tau*0.308*(self.teta/self.tau)**0.929)