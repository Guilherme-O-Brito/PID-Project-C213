import scipy.io
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any

def load_dataset(file_path: str) -> Dict[str, Any]:
    """Carrega e processa o dataset do arquivo MATLAB"""
    try:
        data = scipy.io.loadmat(file_path)
        
        # Extrair os dados principais
        tempo = data['tempo'].flatten()
        entrada = data['entrada'].flatten()
        saida = data['salida'].flatten()  # Note: é 'salida' no arquivo
        
        # Extrair parâmetros do sistema se disponíveis
        params = {}
        if 'parametros_sistema' in data:
            param_struct = data['parametros_sistema']
            if hasattr(param_struct, 'dtype') and param_struct.dtype.names:
                for name in param_struct.dtype.names:
                    params[name] = param_struct[name][0, 0][0, 0]
        
        return {
            'tempo': tempo,
            'entrada': entrada,
            'saida': saida,
            'parametros': params
        }
    except Exception as e:
        print(f"Erro ao carregar dataset: {e}")
        return None

def identify_system_parameters(tempo: np.ndarray, entrada: np.ndarray, saida: np.ndarray) -> Dict[str, float]:
    """Identifica os parâmetros do sistema a partir dos dados"""
    # Implementar identificação de parâmetros
    # Por exemplo, para um sistema de primeira ordem: G(s) = K/(τs + 1)
    
    # Valor final (ganho estático)
    K = np.mean(saida[-10:]) / np.mean(entrada[-10:])
    
    # Tempo de assentamento (63% do valor final)
    valor_final = saida[-1]
    idx_63 = np.where(saida >= 0.63 * valor_final)[0]
    if len(idx_63) > 0:
        tau = tempo[idx_63[0]]
    else:
        tau = 1.0
    
    return {
        'K': K,
        'tau': tau,
        'overshoot': calculate_overshoot(saida),
        'settling_time': calculate_settling_time(tempo, saida)
    }

def calculate_overshoot(saida: np.ndarray) -> float:
    """Calcula o overshoot percentual"""
    valor_final = saida[-1]
    valor_maximo = np.max(saida)
    return ((valor_maximo - valor_final) / valor_final) * 100 if valor_final != 0 else 0

def calculate_settling_time(tempo: np.ndarray, saida: np.ndarray) -> float:
    """Calcula o tempo de assentamento (2% do valor final)"""
    valor_final = saida[-1]
    tolerance = 0.02 * valor_final
    
    # Encontrar último ponto fora da tolerância
    indices_fora = np.where(np.abs(saida - valor_final) > tolerance)[0]
    if len(indices_fora) > 0:
        return tempo[indices_fora[-1]]
    return tempo[0]


import numpy as np
from typing import Tuple, List

class PIDController:
    def __init__(self, kp: float = 1.0, ki: float = 0.0, kd: float = 0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        # Variáveis internas
        self.integral = 0.0
        self.previous_error = 0.0
        self.dt = 0.01  # Tempo de amostragem padrão
        
    def reset(self):
        """Reset do controlador"""
        self.integral = 0.0
        self.previous_error = 0.0
    
    def update(self, setpoint: float, measurement: float) -> float:
        """Atualiza o controlador PID"""
        error = setpoint - measurement
        
        # Termo proporcional
        p_term = self.kp * error
        
        # Termo integral
        self.integral += error * self.dt
        i_term = self.ki * self.integral
        
        # Termo derivativo
        derivative = (error - self.previous_error) / self.dt
        d_term = self.kd * derivative
        
        # Sinal de controle
        control_signal = p_term + i_term + d_term
        
        # Salvar erro para próxima iteração
        self.previous_error = error
        
        return control_signal
    
    def simulate_step_response(self, system_params: dict, time_span: float = 10.0, 
                             setpoint: float = 1.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Simula resposta ao degrau do sistema em malha fechada"""
        dt = 0.01
        t = np.arange(0, time_span, dt)
        
        # Parâmetros do sistema (primeira ordem)
        K = system_params.get('K', 1.0)
        tau = system_params.get('tau', 1.0)
        
        # Arrays para armazenar resultados
        output = np.zeros_like(t)
        control_signal = np.zeros_like(t)
        setpoint_array = np.full_like(t, setpoint)
        
        # Condições iniciais
        self.reset()
        self.dt = dt
        
        for i in range(1, len(t)):
            # Sinal de controle do PID
            u = self.update(setpoint, output[i-1])
            control_signal[i] = u
            
            # Modelo do sistema (primeira ordem)
            # dy/dt = (-y + K*u) / tau
            dydt = (-output[i-1] + K * u) / tau
            output[i] = output[i-1] + dydt * dt
        
        return t, setpoint_array, output, control_signal

def tune_pid_ziegler_nichols(K: float, tau: float, method: str = 'PI') -> dict:
    """Sintoniza PID usando Ziegler-Nichols para sistema de primeira ordem"""
    if method == 'PI':
        kp = 0.9 / K * tau
        ki = kp / (3 * tau)
        kd = 0.0
    elif method == 'PID':
        kp = 1.2 / K * tau  
        ki = kp / (2 * tau)
        kd = kp * tau / 2
    else:  # P only
        kp = 1.0 / K
        ki = 0.0
        kd = 0.0
    
    return {'kp': kp, 'ki': ki, 'kd': kd}