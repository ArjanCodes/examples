from fastapi import HTTPException


class CityNotFoundException(Exception):
    def __init__(self, city_id: int, message: str="City not found"):
        self.city_id = city_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.city_id} -> {self.message}'


class StormNotFoundException(HTTPException):
    def __init__(self, storm_id: int, message: str="Storm not found"):
        self.storm_id = storm_id
        self.message = message
        super().__init__(status_code=404, detail=message)  

    def __str__(self):
        return f'{self.storm_id} -> {self.message}'


class StormAlreadyExistsException(HTTPException):
    def __init__(self, storm_id: int, message: str="Storm already exists"):
        self.storm_id = storm_id
        self.message = message
        super().__init__(status_code=404, detail=message)

    def __str__(self):
        return f'{self.storm_id} -> {self.message}'


class CityAlreadyExistsException(HTTPException):    
    def __init__(self, city_id: int, message: str="City already exists"):
        self.city_id = city_id
        self.message = message
        super().__init__(status_code=404, detail=message)

    def __str__(self):
        return f'{self.city_id} -> {self.message}'
