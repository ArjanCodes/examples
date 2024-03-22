from abc import ABC, abstractmethod
from pickle import dumps as pickle_dumps, loads as pickle_loads
from json import dumps as json_dumps, loads as json_loads

class SerializedFileHandler(ABC):
    def __init__(self, filename):
        self.filename = filename
    @abstractmethod
    def serialize(self, data):
        pass
    
    @abstractmethod
    def deserialize(self, data):
        pass
    
    def write(self, data):
        with open(self.filename, 'wb') as file:
            file.write(self.serialize(data))
            
    def read(self):
        with open(self.filename, 'rb') as file:
            return self.deserialize(file.read())
        
class PickleHandler(SerializedFileHandler):
    def serialize(self, data):
        return pickle_dumps(data)
    
    def deserialize(self, data):
        return pickle_loads(data)
    
class JSONHandler(SerializedFileHandler):
    def serialize(self, data):
        return json_dumps(data).encode('utf-8')
    
    def deserialize(self, data):
        return json_loads(data.decode('utf-8'))
    
def main():
    data = {'name': 'John Doe', 'age': 30}
    pickle_writer = PickleHandler('data.pkl')
    pickle_writer.write(data)
    print(pickle_writer.read())
    
    json_writer = JSONHandler('data.json')
    json_writer.write( data)
    print(json_writer.read())
    
    assert isinstance(pickle_writer, SerializedFileHandler)
    assert isinstance(json_writer, SerializedFileHandler)
    
    
if __name__ == '__main__':
    main()
