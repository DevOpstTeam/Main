from fastapi import FastAPI
import src.database as database

app = FastAPI()

@app.get("/")
def read_root():
    return {"NOVI CICD werkt!"}


@app.get("/db")
def get_data():
    query = "SELECT * FROM meldingen;"
    data = database.getData(query)
    return str({data[0]})