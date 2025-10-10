from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QDoubleSpinBox, QFormLayout, QFileDialog
from PySide6.QtCore import Qt
from ui.widgets.plot_widget import PlotWidget, Curve
from controllers.identificacao_controller import IdentificacaoController

class PageIdentificacao(QWidget):
    def __init__(self, identificacao_controller: IdentificacaoController):
        super().__init__()
        
        self.identificacao_controller = identificacao_controller
        self.file_path = None

        # Layout principal (vertical)
        main_layout = QVBoxLayout()

        # --- texto central ---
        label_title = QLabel('Projeto Prático C213 - Sistemas Embarcados')
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setStyleSheet('font-size: 20px; font-weight: bold; margin-bottom: 20px;')

        # --- layout dos botões (horizontal) ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)  # espaçamento entre os botões

        btn_read = QPushButton('Escolher Arquivo')
        btn_read.setStyleSheet('font-size: 14px; padding: 5px 10px;')

        btn_read.clicked.connect(self.open_file)

        self.file_label = QLabel('Nenhum arquivo selecionado')

        # centraliza os botões horizontalmente
        button_layout.addStretch()
        button_layout.addWidget(btn_read)
        button_layout.addWidget(self.file_label)
        button_layout.addStretch()

        # titulo
        label = QLabel('Dados de Identificação do Sistema por Smith')
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('font-size: 15px; font-weight: semi-bold; margin-bottom: 20px;')

        # --- Layout grafico mais botões ---
        chart_layout = QHBoxLayout()   
        self.plot = PlotWidget(
            title='Resposta do Sistema',
            x_label='Tempo',
            y_label='Amplitude'
        )
        side_form_layout = QVBoxLayout()
        # form
        form = QFormLayout()
        self.k_form = QDoubleSpinBox()
        self.k_form.setMinimum(-9999999)
        self.k_form.setEnabled(False)
        self.k_form.setMaximum(99999999)
        self.tau_form = QDoubleSpinBox()
        self.tau_form.setMinimum(-9999999) 
        self.tau_form.setEnabled(False)
        self.tau_form.setMaximum(99999999)
        self.theta_form = QDoubleSpinBox()
        self.theta_form.setMinimum(-9999999)
        self.theta_form.setEnabled(False)
        self.theta_form.setMaximum(99999999)
        self.eqm_form = QDoubleSpinBox()
        self.eqm_form.setMinimum(-9999999)
        self.eqm_form.setEnabled(False)
        self.eqm_form.setMaximum(99999999)
        form.addRow('K:', self.k_form)
        form.addRow('Tau:', self.tau_form)
        form.addRow('Theta:', self.theta_form)
        form.addRow('EQM:', self.eqm_form)
        export_button = QPushButton('Exportar')
        export_button.clicked.connect(self.plot.export_chart)

        side_form_layout.addLayout(form)
        side_form_layout.addWidget(export_button)

        # --- Montagem final do form ---
        chart_layout.addWidget(self.plot)
        chart_layout.addLayout(side_form_layout)


        # --- Montagem final ---
        main_layout.addStretch()          # empurra tudo para o centro vertical
        main_layout.addWidget(label_title)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()          # empurra tudo para o centro vertical
        main_layout.addWidget(label)
        main_layout.addStretch()          # empurra tudo para o centro vertical
        main_layout.addLayout(chart_layout)

        self.setLayout(main_layout)

    def open_file(self):
        # abre a caixa de dialogo para seleção de arquivos
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Selecione um dataset',
            '',
            'Todos os arquivos (*.*)'
        )
        
        if path:
            # carrega o dataset no controller
            self.identificacao_controller.read_data(path)
            # usa o metodo smith para identificar parametros do sistema
            self.identificacao_controller.identificar_sistema()
            self.file_label.setText(f'Dataset selecionado: {path}')
            self.k_form.setValue(self.identificacao_controller.k)
            self.tau_form.setValue(self.identificacao_controller.tau)
            self.theta_form.setValue(self.identificacao_controller.theta)
            tempo = self.identificacao_controller.tempo
            entrada = self.identificacao_controller.entrada
            saida = self.identificacao_controller.saida
            simulado = self.identificacao_controller.simular()
            # altera o valor do eqm apos simular devido ao eqm ser definido apenas apos a simulação
            self.eqm_form.setValue(self.identificacao_controller.eqm)

            curves = [
                Curve(
                    tempo,
                    saida,
                    'Saida do dataset'
                ),
                Curve(
                    simulado[0],
                    simulado[1],
                    'Saida com modelo SMITH'
                ),
                Curve(
                    tempo,
                    entrada,
                    'Degrau'
                ),
            ]
            
            # Atualiza o gráfico com as novas curvas
            self.plot.update_curves(curves)
            self.curves = curves