from fastapi import FastAPI
import database

app = FastAPI()

@app.get("/")
def read_root():
    return {"NOVI CICD werkt!!"}

@app.get("/db")
def get_data():
    query = "SELECT * FROM meldingen;"
    database.getData(query)
    return{""}