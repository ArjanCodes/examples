from abc import ABC, abstractmethod
class SerializedFileHandler(ABC):
    
    def __init__(self, filename):
        self.filename = filename
    
    @abstractmethod
    def serialize(self, data: dict) -> bytes:
        pass
    
    @abstractmethod
    def deserialize(self, data: bytes) -> dict:
        pass
    
    def write(self, data: dict):
        with open(self.filename, 'wb') as file:
            file.write(self.serialize(data))
            
    def read(self) -> dict:
        with open(self.filename, 'rb') as file:
            return self.deserialize(file.read())
        
def main():
    data = {'name': 'John Doe', 'age': 30}
    file_handler = SerializedFileHandler('data.dat')
    file_handler.write(data)
    print(file_handler.read())
    
if __name__ == '__main__':
    main()
    