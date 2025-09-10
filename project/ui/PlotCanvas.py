from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QSizePolicy
from data.PlotData1D import PlotData1D


class PlotCanvas(FigureCanvas):
    def __init__(self, parent = None, width = 1, height = 1, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, position=[0.15, 0.15, 0.75, 0.75])
        self.axes.grid()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data: PlotData1D):
        self.axes.cla()
        self.axes.grid()
        self.axes.set_title(data.title)
        self.axes.set_xlabel(data.x_label)
        self.axes.set_ylabel(data.y_label)
        #print(len(data.data))
        for i in range(len(data.data)):
            
            self.axes.plot(data.data[i], label=data.labels[i])
        self.axes.legend()
        self.draw()       

    def clear(self):
        self.axes.cla()
        self.axes.grid()
        self.draw()