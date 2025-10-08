import sys
from PySide6.QtWidgets import QApplication
from core.MainWindow import MainWindow
from util.MachineStateManager import MachineStateManager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.connect_manager(MachineStateManager.initialize(window))
    window.show()

    sys.exit(app.exec())

