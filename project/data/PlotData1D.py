
class PlotData1D:
    """
    Klasa koja sadrži podatke koji se odnose na 1D grafike. Služi kao sprega između funkcionalnosti koda koji generišu podatke i PlotCanvas koji koristi ovu klasu za dohvatanje svih grafika koji treba da se prikažu
    """
    def __init__(self, data=None, title="", x_label="", y_label="", labels=None):
        self.data = []
        if data is not None:
            for data_array in data:
                self.data.append(data_array)
            
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        
        self.labels= []
        if labels is not None:
            self.labels = labels
            
    def add_data(self, data, label=None):
        self.data.append(data)
        
        if label is not None:
            self.labels.append(label)
        else:
            self.labels.append("")
        
    def clear_data(self):
        self.data = []
        self.labels = []
        self.title = ""
        self.x_label = ""
        self.y_label = ""
        
        
        