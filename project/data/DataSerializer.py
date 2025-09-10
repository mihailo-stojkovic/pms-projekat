from abc import ABC, abstractmethod



class SerializedDataPackage(ABC):
    """
    Abstraktna klasa koja definiše interfejs za pakete podataka koji se mogu serijalizovati. 
    Svaka konkretna implementacija treba da obezbedi metode za dobijanje podataka i metapodataka, 
    kao i postavljanje klase koja će se koristiti za serijalizaciju paketa.
    """
    def __init__(self, content: dict, serializer_class: type):
        self.serializer_class = serializer_class
        self._content = content
        if not 'metadata' in self.content:
            self.content['metadata'] = {
                'serializer_class': serializer_class.__name__
            }
        else:
            self.content['metadata']['serializer_class'] = serializer_class.__name__
                 
    def get_data(self) -> dict:
        return self.content['data']

    def get_metadata(self) -> dict:
        return self.content['metadata']
    
    def add_metadata(self, key: str, value):
        self.content['metadata'][key] = value

    @abstractmethod
    def is_valid(self) -> bool:
        pass





class DataSerializer(ABC):
    """
    Klasa koja sadrži metode za serijalizaciju i deserijalizaciju podataka. Namena je da olakša čuvanje i učitavanje podataka koji služe aplikaciji kao fajlovi različitih projekata.
    """

    
    @staticmethod
    @abstractmethod
    def serialize(data: SerializedDataPackage, file_path: str) -> str:
        """
        Metoda koja prima podatke i vraća ih u serijalizovanom formatu. Kao izlaz generiše json fajl na zadatoj lokaciji.
        """
        pass

    
    @staticmethod
    @abstractmethod
    def deserialize(file_path: str) -> SerializedDataPackage:
        """
        Metoda koja prima serijalizovane podatke i vraća ih u izvornom formatu. Kao ulaz prima json fajl na zadatoj lokaciji.
        """
        pass
    


class SerializedLocalJsonDataPackage(SerializedDataPackage):
    """
    Klasa koja predstavlja konkretan paket podataka koji se može serijalizovati koristeći LocalDataJsonFormatSerializer.
    """
    def __init__(self, data: dict):
        super().__init__(LocalDataJsonFormatSerializer)
        self._content = data
        
    def is_valid(self) -> bool:
        if not isinstance(self._content, dict):
            return False
        if "data" not in self._content or "metadata" not in self._content:
            return False
        data = self._content["data"]
        if not isinstance(data, dict):
            return False
        required_keys = ["ax", "ay", "az", "v", "koraci"]
        for key in required_keys:
            if key not in data:
                return False
            if key == "koraci":
                if not isinstance(data[key], int):
                    return False
            else:
                if not isinstance(data[key], (int, float)):
                    return False
        return True
    
    
class LocalDataJsonFormatSerializer(DataSerializer):
    
    @staticmethod
    def serialize(data: SerializedDataPackage, file_path: str) -> str:
        import json
        import datetime
        data.add_metadata("timestamp", datetime.datetime.now().isoformat())
        
        with open(file_path, 'w') as f:
            json.dump({
                "metadata": data.get_metadata(),
                "data": data.get_data()
            }, f)
        return file_path



    @staticmethod
    def deserialize(file_path: str) -> SerializedDataPackage:
        import json
        package = None
        with open(file_path, 'r') as f:
            content = json.load(f)
            package = SerializedLocalJsonDataPackage(content)
        if not package.is_valid():
            raise ValueError("Invalid data package")
        return package
    
