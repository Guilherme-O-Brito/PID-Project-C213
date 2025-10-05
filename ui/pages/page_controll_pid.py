from PySide6.QtWidgets import QWidget, QRadioButton, QButtonGroup, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFormLayout, QDoubleSpinBox
from PySide6.QtCore import Qt
from ui.widgets.plot_widget import PlotWidget

class PageControllPID(QWidget):
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

        radio_button_label = QLabel('Seleção de Sintonia: ')

        # Cria dois radio buttons
        opcao1 = QRadioButton("Método Automático")
        opcao2 = QRadioButton("Modo Manual")

        # Agrupa para que apenas um possa ser selecionado
        radio_button = QButtonGroup(self)
        radio_button.addButton(opcao1)
        radio_button.addButton(opcao2)

        # Define um como padrão
        opcao1.setChecked(True)

        button_layout.addStretch()
        button_layout.addWidget(radio_button_label)
        button_layout.addWidget(opcao1)
        button_layout.addWidget(opcao2)
        button_layout.addStretch()

        # --- Lateral Form Layout
        lateral_layout = QVBoxLayout()
        form = QFormLayout()
        self.k_form = QDoubleSpinBox()
        self.k_form.setMinimum(-9999999)
        self.k_form.setEnabled(False)
        self.tau_form = QDoubleSpinBox()
        self.tau_form.setMinimum(-9999999) 
        self.tau_form.setEnabled(False)
        self.theta_form = QDoubleSpinBox()
        self.theta_form.setMinimum(-9999999)
        self.theta_form.setEnabled(False)
        form.addRow("K:", self.k_form)
        form.addRow("Tau:", self.tau_form)
        form.addRow("Theta:", self.theta_form)
        export_button = QPushButton("Exportar")

        lateral_layout.addLayout(form)
        lateral_layout.addWidget(export_button)

        # --- Layout inferior
        inferior_layout = QHBoxLayout()

        self.plot = PlotWidget(
            title='Resposta do Sistema',
            x_label='Tempo',
            y_label='Amplitude'
        )


        inferior_layout.addWidget(self.plot)
        inferior_layout.addLayout(lateral_layout)

        # --- Montagem Final ---
        main_layout.addStretch()
        main_layout.addWidget(label_title)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        main_layout.addLayout(inferior_layout)


        self.setLayout(main_layout)