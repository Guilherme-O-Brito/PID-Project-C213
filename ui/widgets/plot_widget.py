from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout
import numpy as np

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.ax = self.canvas.figure.subplots()
        self.plot_example()

    def plot_example(self):
        t = np.linspace(0, 10, 100)
        y = 1 - np.exp(-t)
        self.ax.plot(t, y)
        self.ax.set_title("Resposta do Sistema")
        self.ax.set_xlabel("Tempo (s)")
        self.ax.set_ylabel("Amplitude")
        self.canvas.draw()