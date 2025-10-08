import threading
from util.StateMachine import StateMachine
from util.SerialComProvider import SerialComProvider
from util.DataManager import DataManager
from util.MachineStates import MachineStates
from data.PlotData1D import PlotData1D
from time import time as tt
import numpy as np
from core.MainWindow import MainWindow
class MachineStateManager:
    __instance = None
    __class_lock = threading.Lock()
    
    __aquisition_lock = threading.Lock()
    __plotter_lock = threading.Lock()
    
    __worker_thread = None
    __peak_thread = None
    __plotter_thread = None
    DETECTION_DELAY = 3  # seconds
    __start_calibration_time = None
    __acceleration_threshold = None
    __steps = 0
    
    def __init__(self, mainWindow : MainWindow = None):
        def __plot_wrapper(data, type):
            mainWindow.update_plot(data, type)
        self.__state_machine = StateMachine.initialize()
        self.__serial_provider = SerialComProvider.initialize()
        self.__main_window = mainWindow
        self.__data_manager = DataManager.initialize(limit=100, plot_function=__plot_wrapper)
      
    @classmethod
    def initialize(cls, mainWindow = None):
    
        def run_worker():
            print("Initializing MachineStateManager worker thread.")
            import time
            meanx, meany, meanz, stdx, stdy, stdz = 0, 0, 0, 0, 0, 0
            while True:
                line = None
                with cls.__instance.__aquisition_lock:
                    line = cls.__instance.__serial_provider.read_line()
                
                if line:
                    parsed = cls.__instance.__serial_provider.parse_line(line)
                    (ax, ay, az, touched) = (
                        float(parsed.get('ax', 0)),
                        float(parsed.get('ay', 0)),
                        float(parsed.get('az', 0)),
                        True if parsed.get('touched', False) == 1 else False)
                    
                    if stdx != 0:
                        ax = 0 if ax < 2*stdx else ax
                        ay = 0 if ay < 2*stdy else ay
                        az = 0 if az < 2*stdz else az
                        
                    MachineStateManager.__instance.__data_manager.add_data_point(ax, 'ax')
                    MachineStateManager.__instance.__data_manager.add_data_point(ay, 'ay')
                    MachineStateManager.__instance.__data_manager.add_data_point(az, 'az')
                    
                    
                    if touched == True:
                        MachineStateManager.__sensor_touched(MachineStateManager.__instance.__data_manager.calibrated())
                    
                    
                    # Kalibracija
                    if cls.__instance.__state_machine.get_state() == MachineStates.STD_CALIBRATION:
                        if tt() - cls.__instance.__start_calibration_time > 3:
                            
                            cls.__instance.__data_manager.calibrate()
                            cls.__instance.__state_machine.set_state(MachineStates.IDLE)
                            calib_data = cls.__instance.__data_manager.get_calibration_data()
                            
                            meanx, meany, meanz, stdx, stdy, stdz = calib_data['ax'], calib_data['ay'], calib_data['az'], calib_data['stdx'], calib_data['stdy'], calib_data['stdz']
                            print(meanx, meany, meanz, stdx, stdy, stdz)
                            
                            mean_mag = np.sqrt(meanx**2 + meany**2 + meanz**2)
                            std_mag = np.sqrt(
                                meanx**2 / mean_mag**2 * stdx**2 +
                                meany**2 / mean_mag**2 * stdy**2 +
                                meanz**2 / mean_mag**2 * stdz**2
                            )
                            
                            cls.__instance.__main_window.apply_threshold(3*std_mag)
                            cls.__instance.__data_manager.plot_histogram_data()
                            
                            print("[WRK-THR] Calibration complete. Switching to IDLE state.")
                    if cls.__instance.__state_machine.get_state() == MachineStates.MEASUREMENT:
                        new_steps = cls.__instance.__data_manager.count_step(cls.__instance.__acceleration_threshold)
                        cls.__instance.__steps += new_steps
                        cls.__instance.__serial_provider.send_command(cls.__instance.__steps)
                        # odradi azuriranje koraka i ovde
                        # ipak ne, to moze u plotter thread   
                        
                time.sleep(0.01)
            
        if not cls.__instance:
            with cls.__class_lock:
                if not cls.__instance:
                    cls.__instance = MachineStateManager(mainWindow=mainWindow)
                    __worker_thread = threading.Thread(target=run_worker, daemon=True)
                    __worker_thread.start()
        return cls.__instance
    
    
    @classmethod
    def cleanup(cls):
        if cls.__instance:
            with cls.__class_lock:
                if cls.__instance:
                    #cleanup entrypoint
                    SerialComProvider.cleanup()
                    DataManager.cleanup()
                    cls.__instance = None
                    
    @classmethod
    def get_state(cls):
        return cls.__instance.__state_machine.get_state()
    
    
    
    @classmethod
    def set_threshold(cls, threshold: float):
        if cls.__instance:
            # Here you can add logic to handle threshold setting
            cls.__instance.__acceleration_threshold = threshold
            print(f"Threshold set to: {threshold}")
        else:
            raise Exception("MachineStateManager not initialized. Call 'initialize' first.")
        
    
    @classmethod
    def set_min_speed(cls, min_speed: float):
        if cls.__instance:
            # Here you can add logic to handle minimum speed setting
            print(f"Minimum speed set to: {min_speed}")
        else:
            raise Exception("MachineStateManager not initialized. Call 'initialize' first.")
        
    @classmethod
    def handle_event(cls, event: str):
        def run_plotter():
            print("Starting plotter thread.")
            import time
            try:
                while True:
                    with cls.__instance.__plotter_lock:
                        cls.__instance.__data_manager.plot_line_data()
                        (last_ax, last_ay, last_az) = cls.__instance.__data_manager.get_latest_data()
                        cls.__instance.__main_window.set_acceleration_labels(last_ax, last_ay, last_az)
                        cls.__instance.__main_window.set_number_of_steps(cls.__instance.__steps)
                    time.sleep(0.1)  # Sleep for a while before next update
            
            except:
                print("Exiting plotter thread.")
        
        if cls.__instance:
            match event:
                case 'sensor_touched':
                    if cls.__instance.__state_machine.get_state() in [MachineStates.INIT, MachineStates.IDLE]:
                        cls.__sensor_touched(cls.__instance.__data_manager.calibrated())
                case 'start_measurement':
                    if cls.__instance.__state_machine.get_state() == MachineStates.IDLE and cls.__instance.__data_manager.calibrated():
                        print("[WRK-THR] Starting measurement...")
                        cls.__instance.__state_machine.set_state(MachineStates.MEASUREMENT)
                        cls.__instance.__data_manager.clear_data()
                        cls.__instance.__plotter_thread = threading.Thread(target=run_plotter, daemon=True)
                        cls.__instance.__plotter_thread.start()
                case 'peak_measurement':
                    if cls.__instance.__state_machine.get_state() == MachineStates.IDLE:
                        cls.__instance.__state_machine.set_state(MachineStates.PEAK_DETECTION)
                        
        else:
            raise Exception("MachineStateManager not initialized. Call 'initialize' first.")
        
        
    @classmethod
    def __sensor_touched(cls, calibrated: bool = False):
        
        def worker_peak_detection():
            print("Starting peak detection thread.")
            import time
            try:
                with cls.__instance.__aquisition_lock:
                    cls.__instance.__data_manager.clear_data()
                time.sleep(MachineStateManager.DETECTION_DELAY)
                # Prikupljeno dovoljno podataka
                cls.__instance.__data_manager.plot_strict_boundary(cls.__instance.__main_window.get_threshold())
                # Pauziraj dalje prikupljanje
                with cls.__instance.__aquisition_lock:
                    cls.__instance.__data_manager.clear_data()
                    cls.__instance.__state_machine.set_state(MachineStates.IDLE)
            except:
                pass
                    
            
            #MachineStateManager.__instance.__state_machine.set_state(MachineStates.IDLE)
            #MachineStateManager.handle_event('start_measurement')
            print("Exiting peak detection thread.")
        
        if cls.__instance:
            if cls.__instance.__state_machine.get_state() not in [
                MachineStates.IDLE, 
                MachineStates.INIT
            ]:
                return
            if calibrated:
                print("[WRK-THR]Device is calibrated. Starting peak detection.")
                cls.__instance.__state_machine.set_state(MachineStates.PEAK_DETECTION)
                cls.__instance.__peak_thread = threading.Thread(target=worker_peak_detection, daemon=True)
                cls.__instance.__peak_thread.start()
            else:
                print("[WRK-THR]Device not calibrated. Starting standard calibration.")
                cls.__instance.__state_machine.set_state(MachineStates.STD_CALIBRATION)
                cls.__instance.__data_manager.clear_data()
                cls.__instance.__start_calibration_time = tt()
                
                
            # Here you can add logic to handle sensor touch event
            print("Sensor touched event handled.")
        else:
            raise Exception("MachineStateManager not initialized. Call 'initialize' first.")
        
        
    @classmethod
    def get_current_state(cls):
        if cls.__instance:
            return cls.__instance.__state_machine.get_state()
        else:
            raise Exception("MachineStateManager not initialized. Call 'initialize' first.")