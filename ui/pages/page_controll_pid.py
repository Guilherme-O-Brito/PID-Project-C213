from PySide6.QtWidgets import QWidget, QRadioButton, QButtonGroup, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFormLayout, QDoubleSpinBox, QComboBox
from PySide6.QtCore import Qt
from ui.widgets.plot_widget import PlotWidget, Curve
from controllers.pid_controller import PIDController
import numpy as np

class PageControllPID(QWidget):
    def __init__(self, pid_controller: PIDController):
        super().__init__()
        self.pid_controller = pid_controller

        # flags para decisão do metodo usado
        self.is_auto = True
        self.method = 'IMC'

        # Layout principal (vertical)
        main_layout = QVBoxLayout()

        # --- texto central ---
        label_title = QLabel('Projeto Prático C213 - Sistemas Embarcados')
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setStyleSheet('font-size: 20px; font-weight: bold; margin-bottom: 20px;')

        # --- layout dos botões (horizontal) ---
        top_layout = QHBoxLayout()
        top_layout.setSpacing(40)  # espaçamento entre os botões

        radio_button_label = QLabel('Seleção de Sintonia: ')

        # cria dois radio buttons
        self.opcao1 = QRadioButton('Método Automático')
        self.opcao2 = QRadioButton('Modo Manual')

        # agrupa para que apenas um possa ser selecionado
        radio_button = QButtonGroup(self)
        radio_button.addButton(self.opcao1)
        radio_button.addButton(self.opcao2)
        
        # define um como padrão
        self.opcao1.setChecked(True)

        self.opcao1.toggled.connect(self.switch_methods)
        self.opcao2.toggled.connect(self.switch_methods)    


        # criando dropdown button para metodos ITAE e IMC
        dropdown_label = QLabel('Selecione o método de sintonia:')
        self.methods = QComboBox()
        self.methods.addItems(['IMC', 'ITAE', 'ZNMA', 'CHR', 'CHR_20', 'CeC'])

        self.methods.currentIndexChanged.connect(self.switch_methods)

        top_layout.addStretch()
        top_layout.addWidget(radio_button_label)
        top_layout.addWidget(self.opcao1)
        top_layout.addWidget(self.opcao2)
        top_layout.addWidget(dropdown_label)
        top_layout.addWidget(self.methods)
        top_layout.addStretch()

        inferior_layout = QHBoxLayout()
        self.plot = PlotWidget(
            title='Sistema com Controle PID',
            x_label='Tempo',
            y_label='Amplitude'
        )
        controll_params_form = QFormLayout()

        # --- Lateral Form Layout
        lateral_layout = QVBoxLayout()
        params_form = QFormLayout()
        
        self.kp_form = QDoubleSpinBox()
        self.kp_form.setMinimum(-9999999)
        self.kp_form.setMaximum(99999999)
        self.ti_form = QDoubleSpinBox()
        self.ti_form.setMinimum(-9999999) 
        self.ti_form.setMaximum(99999999)
        self.td_form = QDoubleSpinBox()
        self.td_form.setMinimum(-9999999)
        self.td_form.setMaximum(99999999)
        self.lambda_form = QDoubleSpinBox()
        self.lambda_form.setMinimum(-9999999)
        self.lambda_form.setMaximum(99999999)
        params_form.addRow('Kp:', self.kp_form)
        params_form.addRow('Ti:', self.ti_form)
        params_form.addRow('Td:', self.td_form)
        params_form.addRow('λ:', self.lambda_form)
        
        # --- buttons layout ---
        buttons_layout = QHBoxLayout()
        export_button = QPushButton('Exportar')
        simulate_button = QPushButton('Sintonizar')
        buttons_layout.addWidget(export_button)
        buttons_layout.addWidget(simulate_button)
        simulate_button.clicked.connect(self.sintonizar)
        export_button.clicked.connect(self.plot.export_chart)

        # --- parametros de controle layout
        self.tr_form = QDoubleSpinBox()
        self.tr_form.setMinimum(-9999999)
        self.tr_form.setMaximum(99999999)
        self.tr_form.setEnabled(False)
        self.ts_form = QDoubleSpinBox()
        self.ts_form.setMinimum(-9999999) 
        self.ts_form.setEnabled(False)
        self.ts_form.setMaximum(99999999)
        self.mp_form = QDoubleSpinBox()
        self.mp_form.setMinimum(-9999999)
        self.mp_form.setEnabled(False)
        self.mp_form.setMaximum(99999999)
        self.erro_form = QDoubleSpinBox()
        self.erro_form.setMinimum(-9999999)
        self.erro_form.setEnabled(False)
        self.erro_form.setMaximum(99999999)
        controll_params_form.addRow('Tr (tempo de subida):', self.tr_form)
        controll_params_form.addRow('Ts (acomodação):', self.ts_form)
        controll_params_form.addRow('Mp (overshoot):', self.mp_form)
        controll_params_form.addRow('Erro em regime permanente:', self.erro_form)

        # --- conectando layouts ---
        lateral_layout.addLayout(params_form)
        lateral_layout.addLayout(buttons_layout)
        lateral_layout.addLayout(controll_params_form)

        # --- layout inferior
        inferior_layout.addWidget(self.plot)
        inferior_layout.addLayout(lateral_layout)

        # --- montagem final ---
        main_layout.addStretch()
        main_layout.addWidget(label_title)
        main_layout.addLayout(top_layout)
        main_layout.addStretch()
        main_layout.addLayout(inferior_layout)


        self.setLayout(main_layout)

        # chama o metodo ao final da construção da classe para iniciar em modo automatico
        self.switch_methods()

    def switch_methods(self):
        if self.opcao1.isChecked():
            self.kp_form.setEnabled(False)
            self.ti_form.setEnabled(False)
            self.td_form.setEnabled(False)
            self.methods.setEnabled(True)
            self.method = self.methods.currentText()
            if self.method == 'IMC':
                self.lambda_form.setEnabled(True)
            else: 
                self.lambda_form.setEnabled(False)
                self.lambda_form.setValue(0)
            self.is_auto = True
        else:
            self.kp_form.setEnabled(True)
            self.ti_form.setEnabled(True)
            self.td_form.setEnabled(True)
            self.lambda_form.setEnabled(False)
            self.lambda_form.setValue(0)
            self.methods.setEnabled(False)
            self.is_auto = False
            

    def sintonizar(self):
        
        if self.is_auto:
            # sintonia automatica
            lamb = self.lambda_form.value()
            results = self.pid_controller.auto_sintonizar(self.method, lamb)
            sintonia = results['sintonia']
            [kp, ti, td, lamb] = results['params']
            [tr, ts, mp, steady_value, ess] = results['controll_params']
            # atualizando forms
            self.kp_form.setValue(kp)
            self.ti_form.setValue(ti)
            self.td_form.setValue(td)
            self.lambda_form.setValue(lamb)
        else:
            # sintonia manual 
            kp = self.kp_form.value()
            ti = self.ti_form.value()
            td = self.td_form.value()
            results = self.pid_controller.sintonizar(kp, ti, td)
            sintonia = results['sintonia']
            [kp, ti, td] = results['params']
            [tr, ts, mp, steady_value, ess] = results['controll_params']

        # atualiza valores dos formularios apos sintonia
        self.tr_form.setValue(tr)
        self.ts_form.setValue(ts)
        self.mp_form.setValue(mp)
        self.erro_form.setValue(ess)

        # atualiza as curvas de sintonia        
        curves = [
            Curve(
                sintonia[0],
                sintonia[1],
                'PID'
            ),
            Curve(
                sintonia[0],
                np.zeros_like(sintonia[0]) + steady_value,
                'Valor de Acomodação',
                '--'
            ),
        ]

        self.plot.update_curves(curves)

