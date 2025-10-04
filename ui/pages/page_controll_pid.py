from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFormLayout, QDoubleSpinBox
from ui.widgets.plot_widget import PlotWidget

class PageControllPID(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        form = QFormLayout()

        self.kp = QDoubleSpinBox(); self.kp.setValue(0.6)
        self.ti = QDoubleSpinBox(); self.ti.setValue(1.0)
        self.td = QDoubleSpinBox(); self.td.setValue(0.1)
        form.addRow("Kp:", self.kp)
        form.addRow("Ti:", self.ti)
        form.addRow("Td:", self.td)

        self.plot = PlotWidget()
        self.btn = QPushButton("Simular")

        layout.addLayout(form)
        layout.addWidget(self.plot)
        layout.addWidget(self.btn)

        self.setLayout(layout)