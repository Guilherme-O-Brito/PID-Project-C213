from PySide6.QtWidgets import QMainWindow, QTabWidget
from ui.pages.page_inicio import PageInicio
from ui.pages.page_identificacao import PageIdentificacao
from ui.pages.page_controll_pid import PageControllPID
from controllers.identificacao_controller import IdentificacaoController
from controllers.pid_controller import PIDController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        identificacao_controller = IdentificacaoController()
        pid_controller = PIDController()
        identificacao_controller.pid_controller = pid_controller

        self.setWindowTitle('Projeto Prático C213 - Sistemas Embarcados')

        self.tabs = QTabWidget()
        self.tabs.addTab(PageInicio(), 'Início')
        self.tabs.addTab(PageIdentificacao(identificacao_controller), 'Identificação')
        self.tabs.addTab(PageControllPID(pid_controller), 'Controle PID')

        self.setCentralWidget(self.tabs)
