from PySide6.QtWidgets import QMainWindow, QTabWidget
#from ui.pages.page_ import PageInicio
from ui.pages.page_identificacao import PageIdentificacao
from ui.pages.page_controll_pid import PageControllPID
from controllers.identificacao_controller import IdentificacaoController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        identificacao_controller = IdentificacaoController()

        self.setWindowTitle("Projeto Prático C213 - Sistemas Embarcados")

        self.tabs = QTabWidget()
        #self.tabs.addTab(PageInicio(), "Início")
        self.tabs.addTab(PageIdentificacao(identificacao_controller), "Identificação")
        self.tabs.addTab(PageControllPID(), "Controle PID")

        self.setCentralWidget(self.tabs)
