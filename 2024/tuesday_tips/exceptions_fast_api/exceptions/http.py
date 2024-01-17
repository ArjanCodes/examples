from fastapi import HTTPException


class CityNotFoundException(HTTPException):
    def __init__(self, message: str="City not found"):
        self.message = message
        super().__init__(status_code=404, detail=message)


class StormNotFoundException(HTTPException):
    def __init__(self, message: str="Storm not found"):
        self.message = message
        super().__init__(status_code=404, detail=message)  

class StormAlreadyExistsException(HTTPException):
    def __init__(self, message: str="Storm already exists"):
        self.message = message
        super().__init__(status_code=404, detail=message)


class CityAlreadyExistsException(HTTPException):    
    def __init__(self, message: str="City already exists"):
        self.message = message
        super().__init__(status_code=404, detail=message)
