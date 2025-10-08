import threading
import numpy as np


class DataManager:
    
    __instance = None
    __class_lock = threading.Lock()
    
    
    def __init__(self, limit: int = 100, plot_function = None):
        self.__data_lock = threading.Lock()
        self.__data = {}
        self.__limit = limit
        self.__calibration_values = {}
        self.__calibrated = False
        self.__plot_function = plot_function
        
    
    @classmethod
    def initialize(cls, limit: int = 100, plot_function = None):
        if not cls.__instance:
            with cls.__class_lock:
                if not cls.__instance:
                    cls.__instance = DataManager(limit, plot_function=plot_function)
        return cls.__instance
    
    @classmethod
    def get_data(cls, key: str = 'default') -> list[float]:
        if cls.__instance:
            with cls.__instance.__data_lock:
                return cls.__instance.__data.get(key, []).copy()
        else:
            raise Exception("DataManager not initialized. Call 'initialize' first.")
        
        
    @classmethod
    def add_data_point(cls, point: float, key: str = 'default'):
        if cls.__instance:
            with cls.__instance.__data_lock:
                _point = point
                if cls.__instance.__calibrated and key in ['ax', 'ay', 'az']:
                    _point = point - cls.__instance.__calibration_values[key]
                if key not in cls.__instance.__data:
                    cls.__instance.__data[key] = []
                cls.__instance.__data[key].append(_point)
                # Maintain size limit
                if len(cls.__instance.__data[key]) > cls.__instance.__limit:
                    cls.__instance.__data[key].pop(0)
                    #print(f"Number of elements in array {key} is {len(cls.__instance.__data[key])}")
        else:
            raise Exception("DataManager not initialized. Call 'initialize' first.")
        
        
    @classmethod
    def cleanup(cls):
        if cls.__instance:
            with cls.__class_lock:
                if cls.__instance:
                    cls.__instance = None
                    
                    
    @classmethod
    def can_calibrate(cls) -> bool:
        return True
    
    @classmethod
    def calibrated(cls) -> bool:
        if cls.__instance:
            return cls.__instance.__calibrated
        else:
            raise Exception("DataManager not initialized. Call 'initialize' first.")
    
    @classmethod
    def clear_data(cls):
        if cls.__instance:
            with cls.__instance.__data_lock:
                cls.__instance.__data.clear()
        else:
            raise Exception("DataManager not initialized. Call 'initialize' first.")
    
    
    @classmethod
    def get_calibration_data(cls) -> list[float]:
        if cls.__instance:
            print("Calculating calibration data...")
            #check first if calibration data already is calculated
            if cls.__instance.__calibration_values:
                return cls.__instance.__calibration_values
            calibration_return = {'ax': 0.0, 'ay': 0.0, 'az': 0.0}
            for key in ['x', 'y', 'z']:
                calibration_return['a' + key] = np.mean(cls.__instance.__data.get('a' + key, []))
                calibration_return['std' + key] = np.std(cls.__instance.__data.get('a' + key, []))
            cls.__instance.__calibration_values = calibration_return
            return calibration_return
        else:
            raise Exception("DataManager not initialized. Call 'initialize' first.")
    
    @classmethod
    def calibrate(cls):
        if cls.__instance:
            with cls.__instance.__data_lock:
                print("Attempting to calibrate...")
                if cls.can_calibrate():
                    print("Calculating calibration values...")
                    cls.__instance.__calibration_values = cls.get_calibration_data()
                    cls.__instance.__data.pop('calx', None)
                    cls.__instance.__data.pop('caly', None)
                    cls.__instance.__data.pop('calz', None)
                    print(f"Calibration values set to: {cls.__instance.__calibration_values}")
                    cls.__instance.__calibrated = True
                    return cls.__instance.__calibration_values
        else:
            raise Exception("DataManager not initialized. Call 'initialize' first.")
      
      
      
        
    
    @classmethod 
    def to_plotdata(cls, 
                    title : str = "Podaci ubrzanja u realnom vremenu", 
                    x_label : str ="Redni broj", 
                    y_label : str ="Ubrzanje[a.u.]", 
                    labels : list = ['ax', 'ay', 'az'],
                    func_type : str = "value"
                    ):
        from data.PlotData1D import PlotData1D
        ax, ay, az = cls.__instance.get_data('ax'), cls.__instance.get_data('ay'), cls.__instance.get_data('az')
        if func_type == "derivative":
            ax, ay, az = np.diff(ax), np.diff(ay), np.diff(az)
        plotData = PlotData1D(
            title=title,
            x_label=x_label,
            y_label=y_label,
            data=[ax, ay, az],
            labels=labels
        )
        print("Packaging plotdata")
        return plotData

    
    @classmethod
    def __get_histogram_packet(cls):
        return cls.__instance.to_plotdata(x_label="Ubrzanje[a.u.]", y_label="Frekvencija", title="Histogram kalibracionih merenja akcelerometra")
                
        
        
    @classmethod
    def plot_histogram_data(cls):
        if cls.__instance:
            cls.__instance.__plot_function(
                cls.__instance.__get_histogram_packet(),
                'hist'
            )
        else:
            raise Exception("DataManager not initialized. Call 'initialize' first.")
    
    @classmethod
    def plot_line_data(cls, func_type : str = 'value'):
        if cls.__instance:
            print("Attempting to plot from DataManager")
            cls.__instance.__plot_function(
                cls.__instance.to_plotdata(func_type=func_type),
                'line'
            )
        else:
            raise Exception("DataManager not initialized. Call 'initialize' first.")
      
      
    @classmethod
    def plot_strict_boundary(cls, threshold : int = 0):
        from data.PlotData1D import PlotData1D
        (ax, ay, az) = (np.array(cls.__instance.get_data('ax')),
                        np.array(cls.__instance.get_data('ay')),
                        np.array(cls.__instance.get_data('az')))
        
        ax = np.where(ax>threshold, 1024 - cls.__instance.__calibration_values['ax'], 0)
        ay = np.where(ay>threshold, 1024 - cls.__instance.__calibration_values['ay'], 0)
        az = np.where(az>threshold, 1024 - cls.__instance.__calibration_values['az'], 0)
        plotData = PlotData1D(
            title="Merenje ubrzanja sa jasnim presekom",
            x_label="redni broj merenja",
            y_label="Ubrzanje[a.u.]",
            data=[ax, ay, az],
            labels=['ax', 'ay', 'az']
        )
        cls.__instance.__plot_function(plotData, 'line')
        
        
          
    @classmethod
    def get_latest_data(cls):
        if cls.__instance:
            if len(cls.__instance.get_data('ax')) == 0:
                return (0,0,0)
            return (cls.__instance.get_data('ax')[-1],
                    cls.__instance.get_data('ay')[-1],
                    cls.__instance.get_data('az')[-1],)
        else:
            raise Exception("DataManager not initialized. Call 'initialize' first.")
        
        
    @classmethod
    def count_step(cls, threshold : int = 0):
        print("Counting number of steps")
        is_step = lambda x: x[0] > x[1]
        if cls.__instance:
            (ax, ay, az) = (np.array(cls.__instance.get_data('ax')),
                    np.array(cls.__instance.get_data('ay')),
                    np.array(cls.__instance.get_data('az')))
            if len(ax) < 2:
                return 0        
            ax = np.array(ax[-2:])
            ay = np.array(ay[-2:])
            az = np.array(az[-2:])
            ax = np.where(ax > threshold, 1024 - cls.__instance.__calibration_values['ax'], 0)
            ay = np.where(ay > threshold, 1024 - cls.__instance.__calibration_values['ay'], 0)
            az = np.where(az > threshold, 1024 - cls.__instance.__calibration_values['az'], 0)    

            count = 0
            count += 1 if is_step(ax) == True else 0
            count += 1 if is_step(ay) == True else 0
            count += 1 if is_step(az) == True else 0
            return count
