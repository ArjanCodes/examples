import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ResponseModel(BaseModel):
    message: str


@app.get("/hello", response_model=ResponseModel)
def hello(name: str = "World"):
    return {"message": f"Hello, {name}!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
