from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QDoubleSpinBox, QFormLayout
from PySide6.QtCore import Qt
from ui.widgets.plot_widget import PlotWidget

class PageReadDataset(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal (vertical)
        main_layout = QVBoxLayout()

        # --- Texto central ---
        label_title = QLabel("Projeto Prático C213 - Sistemas Embarcados")
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")

        # --- Layout dos botões (horizontal) ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)  # Espaçamento entre os botões

        btn_identificacao = QPushButton("Escolher Arquivo")

        btn_identificacao.setStyleSheet("font-size: 14px; padding: 5px 10px;")

        # Centraliza os botões horizontalmente
        button_layout.addStretch()
        button_layout.addWidget(btn_identificacao)
        button_layout.addStretch()

        # Titulo
        label = QLabel("Dados de Identificação do Sistema")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 15px; font-weight: semi-bold; margin-bottom: 20px;")

        # --- Layout grafico mais botões ---
        grafic_layout = QHBoxLayout()   
        side_form_layout = QVBoxLayout()
        # form
        form = QFormLayout()
        Ks = QDoubleSpinBox()
        Ks.setMinimum(-9999999)
        Ts = QDoubleSpinBox()
        Ts.setMinimum(-9999999) 
        Os = QDoubleSpinBox()
        Os.setMinimum(-9999999)
        Es = QDoubleSpinBox()
        Es.setMinimum(-9999999)
        form.addRow("KS:", Ks)
        form.addRow("Ts:", Ts)
        form.addRow("Ωs:", Os)
        form.addRow("Es:", Es)
        export_button = QPushButton("Exportar")

        side_form_layout.addLayout(form)
        side_form_layout.addWidget(export_button)

        # --- Montagem final do form ---
        plot = PlotWidget()
        grafic_layout.addWidget(plot)
        grafic_layout.addLayout(side_form_layout)


        # --- Montagem final ---
        main_layout.addStretch()          # empurra tudo para o centro vertical
        main_layout.addWidget(label_title)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()          # empurra tudo para o centro vertical
        main_layout.addWidget(label)
        main_layout.addStretch()          # empurra tudo para o centro vertical
        main_layout.addLayout(grafic_layout)

        self.setLayout(main_layout)