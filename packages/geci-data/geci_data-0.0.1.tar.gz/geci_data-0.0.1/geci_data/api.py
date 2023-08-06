from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_main():
    return {"msg": "Hello World"}

@app.get("/api/v1/data")
def give_data():
    return {"data": "datos"}
