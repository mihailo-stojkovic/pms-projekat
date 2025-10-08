import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import QObject, Signal, Slot
from data.PlotData1D import PlotData1D


class PlotCanvas(pg.GraphicsLayoutWidget):
    class PlotSignal(QObject):
        trigger = Signal(object)  # carries a PlotData1D object

    def __init__(self, parent=None, plot_type: str = "line", overlay: bool = False):
        super().__init__(parent=parent, show=True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Signal setup
        self._plot_signal = PlotCanvas.PlotSignal()
        self._plot_signal.trigger.connect(self._do_plot)

        # Color cycle
        self._colors = ['r', 'g', 'b', 'c', 'm', 'y', 'w']

        # Settings
        self.plot_type = plot_type
        self.overlay = overlay

        # Track global min/max for line plots only
        self._y_min_global = None
        self._y_max_global = None

    def set_plot_type(self, plot_type: str):
        if plot_type not in ("line", "hist"):
            raise ValueError("plot_type must be 'line' or 'hist'")
        self.plot_type = plot_type

    def set_overlay(self, overlay: bool):
        self.overlay = overlay

    def plot(self, data: PlotData1D):
        self._plot_signal.trigger.emit(data)

    @Slot(object)
    def _do_plot(self, data: PlotData1D):
        # Update global min/max only for line plots, safely skipping empty curves
        if self.plot_type == "line":
            non_empty_curves = [np.array(curve) for curve in data.data if len(curve) > 0]
            if non_empty_curves:
                data_min = min(curve.min() for curve in non_empty_curves)
                data_max = max(curve.max() for curve in non_empty_curves)

                if self._y_min_global is None or data_min < self._y_min_global:
                    self._y_min_global = data_min
                if self._y_max_global is None or data_max > self._y_max_global:
                    self._y_max_global = data_max

        # Clear old layout
        self.clear()

        if self.overlay:
            plot_item = self.addPlot(title=data.title)
            plot_item.showGrid(x=True, y=True)
            legend = plot_item.addLegend(offset=(-30, 30))

            # Apply historical y-limits only for line plots
            if self.plot_type == "line" and self._y_min_global is not None:
                plot_item.setYRange(self._y_min_global, self._y_max_global)

            for i, curve in enumerate(data.data):
                color = self._colors[i % len(self._colors)]
                label = data.labels[i] if i < len(data.labels) else None

                if self.plot_type == "line" and len(curve) > 0:
                    pen = pg.mkPen(color=color, width=2)
                    x = np.arange(len(curve))
                    item = plot_item.plot(x, curve, pen=pen, name=label)

                elif self.plot_type == "hist" and len(curve) > 0:
                    y, edges = np.histogram(curve, bins=30)
                    centers = 0.5 * (edges[:-1] + edges[1:])
                    width = edges[1] - edges[0]
                    bg = pg.BarGraphItem(x=centers, height=y, width=width, brush=color)
                    plot_item.addItem(bg)
                    item = bg

                if label and self.plot_type == "line":
                    legend.addItem(item, label)

        else:
            for i, curve in enumerate(data.data):
                plot_item = self.addPlot(
                    row=i, col=0,
                    title=f"{data.title} - {data.labels[i] if i < len(data.labels) else f'Curve {i+1}'}"
                )
                plot_item.showGrid(x=True, y=True)

                # Apply historical y-limits only for line plots
                if self.plot_type == "line" and self._y_min_global is not None:
                    plot_item.setYRange(self._y_min_global, self._y_max_global)

                color = self._colors[i % len(self._colors)]

                if self.plot_type == "line" and len(curve) > 0:
                    pen = pg.mkPen(color=color, width=2)
                    x = np.arange(len(curve))
                    plot_item.plot(x, curve, pen=pen)

                elif self.plot_type == "hist" and len(curve) > 0:
                    y, edges = np.histogram(curve, bins=30)
                    centers = 0.5 * (edges[:-1] + edges[1:])
                    width = edges[1] - edges[0]
                    bg = pg.BarGraphItem(x=centers, height=y, width=width, brush=color)
                    plot_item.addItem(bg)

    def clear(self):
        # Remove all plots
        self.ci.clear()
