from scipy.io import loadmat
import pandas as pd

annots = loadmat('Dataset_Grupo7_c213.mat')

x_data = annots['dados_saida'][:, 0]  
y_data = annots['dados_saida'][:, 1]  

df = pd.DataFrame({
    'tempo': x_data,
    'resposta': y_data
})

print(df)