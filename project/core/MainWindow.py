from PySide6.QtWidgets import QMainWindow
from ui.UI_Window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Button actions
        self.ui.buttonStart.clicked.connect(self.start_action)
        self.ui.buttonStop.clicked.connect(self.stop_action)
        #self.ui.buttonPragPrimeni.clicked.connect(self.apply_threshold)
        #self.ui.buttonMinPrimeni.clicked.connect(self.apply_min_speed)
        
        
    def update_plot(self, data):
        self.ui.plotWidget.plot(data)

    def start_action(self):
        """
        Akcija koja se izvršava kada se pritisne dugme "Start"
        """
        print("Start button clicked")
        import numpy as np
        from data.PlotData1D import PlotData1D
        x = np.sin(np.linspace(0, 10, 1000)) + np.random.normal(0, 0.5, 1000)
        y = np.cos(np.linspace(0, 10, 1000)) + np.random.normal(0, 0.5, 1000)
        plotData = PlotData1D(data=[x, y], title="Naslov", x_label="X osa", y_label="Y osa", labels=["sin(x)", "cos(x)"])
        self.update_plot(plotData)
        self.ui.lcdNumberBrzina.display(self.ui.lcdNumberBrzina.value()+1)
        
    def stop_action(self):
        print("Stop button clicked")
        self.ui.plotWidget.clear()