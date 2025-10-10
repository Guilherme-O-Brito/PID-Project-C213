from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QMessageBox
import numpy as np

class Curve:
    def __init__(
            self, 
            x_axix: np.ndarray,
            y_axis: np.ndarray,
            label: str,
            params: str = '' 
        ):
        self.x_axis = x_axix
        self.y_axis = y_axis
        self.label = label
        self.params = params
        assert self.x_axis.shape == self.y_axis.shape
        

class PlotWidget(QWidget):
    def __init__(
            self, 
            curves: list[Curve] = [],
            title: str = '',
            x_label: str = '',
            y_label: str = ''
        ):
        super().__init__()
        self.curves = curves
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        

        layout = QVBoxLayout()
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.ax = self.canvas.figure.subplots()
        self.canvas.figure.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.9)
        self.plot_chart()

    def plot_chart(self):
        self.ax.clear()  # Limpa o gráfico anterior
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        for curve in self.curves:
            self.ax.plot(curve.x_axis, curve.y_axis, curve.params, label=curve.label)
        if self.curves:
            self.ax.legend()
            self.ax.grid()
        self.canvas.draw()
    
    def update_curves(self, curves: list[Curve]):
        # atualiza as curvas e redesenha o gráfico
        self.curves = curves
        self.plot_chart()

    def export_chart(self):

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            'Salvar gráfico como . . .',
            '', # diretorio inicial = ao diretorio atual
            'Imagens (*.png *.jpg *.jpeg *.pdf *.svg)'  # filtros de extensão
        )

        # garante que o caminho foi selecionado
        if save_path:
            try:
                self.canvas.figure.savefig(save_path, dpi=800, bbox_inches='tight')
                QMessageBox.information(self, 'Sucesso', f'Gráfico salvo  em:\n{save_path}')
            except Exception as e:
                QMessageBox.critical(self, 'Erro', f'Falha ao salvar gráfico:\n{e}')