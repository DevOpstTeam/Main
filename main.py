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
<<<<<<< HEAD
    return str({data[0]})
=======
    msg = f'\tMESSAGE\n{data[0]["id"]}\n{data[0]["ABP"]}\n{data[0]["Postcode"]}'
    return{msg}
>>>>>>> origin/dev
