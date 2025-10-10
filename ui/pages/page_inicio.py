from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class PageInicio(QWidget):
    def __init__(self):
        super().__init__()

        # ---------- Layout principal ----------
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(30)

        # ---------- título ----------
        title = QLabel('Projeto de Controle - Sintonia PID')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # ---------- descrição ----------
        description = QLabel(
            'Este projeto tem como objetivo realizar a identificação e sintonia de um '
            'sistema de controle utilizando controladores PID. A interface permite '
            'carregar dados experimentais, identificar os parâmetros da planta com metodo de SMITH, aplicar '
            'métodos de sintonia clássicos e analisar a resposta do sistema controlado.'
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setFont(QFont('Arial', 12))
        main_layout.addWidget(description)

        # ---------- nomes dos integrantes ----------
        members_label = QLabel('Integrantes do grupo:')
        members_label.setFont(QFont('Arial', 14, QFont.Weight.Medium))
        members_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        members_box = QLabel(
            'Eduardo Augusto\n'
            'Guilherme Brito\n'
            'João Gabriel\n'
        )
        members_box.setFont(QFont('Arial', 11))
        members_box.setAlignment(Qt.AlignmentFlag.AlignLeft)

        main_layout.addWidget(members_label)
        main_layout.addWidget(members_box)

        self.setLayout(main_layout)