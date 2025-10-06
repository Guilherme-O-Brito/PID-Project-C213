from core.utils import *
import control as ctrl

class IdentificacaoController:
    def __init__(self):
        self.data = None
        self.k = 0
        self.tau = 0
        self.theta = 0
        self.eqm = 0
        self.eqm_atraso = 0

    '''
        Realiza a leitura dos dados atraves de um dataset
        o parametro path deve ser uma string contendo o caminho absoluto ate o 
        dataset
    '''
    def read_data(self, path: str):
        # Importando o dataset com o caminho dado
        dataset = loadmat(path)
        
        # Separando os dados lidos em arrays do numpy 
        dados_entrada = np.array(dataset['dados_entrada'])
        dados_saida = np.array(dataset['dados_saida'])
        tempo = np.array(dataset['tiempo'])[0, :]
        entrada = np.array(dataset['entrada'])[0, :]
        saida = np.array(dataset['salida'])[0, :]
        parametros = dataset['parametros_sistema']

        self.data = {
            'dados_entrada': dados_entrada,
            'dados_saida': dados_saida,
            'tempo': tempo,
            'entrada': entrada,
            'saida': saida,
            'parametros': parametros
        }

    '''
        Realiza a identificação do sistema usando metodo smith
    '''
    def identificar_sistema(self):
        if self.data:
            # recupera os dados do dataset 
            self.saida = self.data['saida']
            self.entrada = self.data['entrada']
            self.tempo = self.data['tempo']
            
            self.k = (self.saida[-1] - self.saida[0]) / self.entrada[0]
            # Encontra tempos para 28.3% e 63.2% da resposta
            t1 = self.tempo[self.saida >= 0.283 * self.saida[-1]][0]
            t2 = self.tempo[self.saida >= 0.632 * self.saida[-1]][0]
            # τ e θ pelo método da tangente aproximado
            self.tau = 1.5 * (t2 - t1)
            self.theta = t2 - self.tau
        else:
            raise DataNotInitialized()

    def simular(self):
        if self.data:
            # cria o sistema simulado com base nos parametros identificados no dataset
            sys = ctrl.tf([self.k], [self.tau, 1])
            [num, den] = ctrl.pade(self.theta, 3)
            sys_pade = ctrl.tf(num, den)
            sys_atraso = ctrl.series(sys, sys_pade)
            simulado = np.array(ctrl.forced_response(sys, T=self.tempo, U=self.entrada))
            atraso_simulado = np.array(ctrl.forced_response(sys_atraso, T=self.tempo, U=self.entrada))
            self.eqm = np.sqrt(np.mean(simulado[1] - self.saida)**2)
            self.eqm_atraso = np.sqrt(np.mean(atraso_simulado[1] - self.saida)**2)
            
            return [simulado, atraso_simulado]
        else:
            raise DataNotInitialized()

class DataNotInitialized(Exception):
    def __init__(self):
        self.mensagem = 'Data não foi inicializado'
        super().__init__(self.mensagem)
        