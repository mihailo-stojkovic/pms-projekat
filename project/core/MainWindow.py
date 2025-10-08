from data.PlotData1D import PlotData1D
from PySide6.QtWidgets import QMainWindow
from ui.UI_Window import Ui_MainWindow
class MainWindow(QMainWindow):
    # add qt thread to handle getting data from the arduino
    
    state = None
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Button actions
        self.ui.buttonStart.clicked.connect(self.start_action)
        self.ui.buttonStop.clicked.connect(self.stop_action)
        self.ui.buttonPragPrimeni.clicked.connect(self.apply_threshold)
        self.ui.buttonMinPrimeni.clicked.connect(self.apply_min_speed)
        
        
        
        
    def update_plot(self, data, plot_type: str = "line"):
        self.ui.plotWidget.set_plot_type(plot_type)
        self.ui.plotWidget.plot(data)
        
        
    def set_acceleration_labels(self, ax, ay, az):
        self.ui.lcdNumberAx.display(ax)
        self.ui.lcdNumberAy.display(ay)
        self.ui.lcdNumberAz.display(az)
        
        
    def set_current_speed(self, speed):
        self.ui.lcdNumberBrzina.display(speed)

    def set_number_of_steps(self, steps):
        self.ui.lcdNumberBrojKoraka.display(steps)

    def start_action(self):
        """
        Akcija koja se izvršava kada se pritisne dugme "Start"
        """
        self.state.handle_event("start_measurement")
        # Prelazak iz idle u measurement
        
    def get_threshold(self):
        return float(self.ui.lineEditPrag.text())
    
    def get_minimal_speed(self):
        return float(self.ui.lineEditMin.text())
    
    def stop_action(self):
        #Stop treba da prebaci iz measurement u idle
        
        pass
            
        self.ui.plotWidget.clear()
        
    def apply_threshold(self, value : float = None):
        try:
            _value = value
            if value is None:
                _value = float(self.ui.lineEditPrag.text())
            else:
                self.ui.lineEditPrag.setText(str(value))
            threshold_value = _value
            if MainWindow.state:
                MainWindow.state.set_threshold(threshold_value)
            print(f"Threshold applied: {threshold_value}")
        except:
            pass
        
    def apply_min_speed(self, value : float =None):
        try:
            _value = value
            if value is None:
                _value = float(self.ui.lineEditMin.text())
            else:
                self.ui.lineEditMin.setText(str(value))
            min_speed_value = _value
            if MainWindow.state:
                MainWindow.state.set_min_speed(min_speed_value)
            print(f"Minimum speed applied: {min_speed_value}")
    
        except:
            pass
        
    def connect_manager(self, manager):
        self.state = manager
    
    def closeEvent(self, event):
        self.state.cleanup()