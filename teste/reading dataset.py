import scipy.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = scipy.io.loadmat('C:\\Users\\Guilherme\\OneDrive\\Documents\\Inatel\\C213 - PID\\PID-Project-C213\\core\\Dataset_Grupo7_c213.mat')

dados_entrada = np.array(pd.DataFrame(data['dados_entrada']))
dados_saida = np.array(pd.DataFrame(data['dados_saida']))
tempo = np.array(pd.DataFrame(data['tiempo']))[0, :]
entrada = np.array(pd.DataFrame(data['entrada']))[0, :]
saida = np.array(pd.DataFrame(data['salida']))[0, :]
parametros = data['parametros_sistema']

'''plt.plot(dados_saida[:,0], dados_saida[:,1], label='Saida')
plt.plot(dados_entrada[:,0], dados_entrada[:,1], label='Entrada')
plt.grid()
plt.legend()
plt.show()'''

k = (saida[-1] - saida[0]) / entrada[0]
# Normaliza resposta
y_norm = (saida - saida[0]) / entrada[0]

# Encontra tempos para 28.3% e 63.2% da resposta
#t1 = tempo[np.argmin(np.abs(y_norm - 0.283))]
#t2 = tempo[np.argmin(np.abs(y_norm - 0.632))]

t1 = tempo[saida >= 0.283 * saida[-1]][0]
t2 = tempo[saida >= 0.632 * saida[-1]][0]
print(t1)
# τ e θ pelo método da tangente aproximado
tau = 1.5 * (t2 - t1)
teta = t2 - tau

print(f'k = {k}, Tau = {tau}, Teta = {teta}')

print(parametros.shape)
for param in parametros:
    print(param)
