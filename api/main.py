from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Responder(BaseModel):
    name: str
    location: str
    body_temp: int
    blood_oxygen: int

# employees information
responders = {
    1 : {"name": "John Doe","location": "Somewhere","body_temp": 98,"blood_oxygen": 99},
    2 : {"name": "Mickey Mouse","location": "Disney","body_temp": 99,"blood_oxygen": 100},
    3 : {"name": "Scooby Doo","location": "Dog house","body_temp": 96,"blood_oxygen": 98.5},
    4 : {"name": "Lighning McQueen","location": "Racetrack","body_temp": 104,"blood_oxygen": 97},
    5 : {"name": "Olaf","location": "Arendelle","body_temp": 20,"blood_oxygen": 10},
    6 : {"name": "Buzz Lightyear","location": "Sunnyside Daycare","body_temp": 98,"blood_oxygen": 88}
}

# Create an endpoint
@app.get("/")
def home():
    return {"name" : "Telemetry Data App", "version": "1.0.0"}

# Responders REST APIs
@app.get("/responders")
def allResponders():
    return responders

@app.get("/responders/by-id/{respId}")
def respById(respId: int = Path(None, description = "Enter valid responder id", gt = 0, lt = len(responders) + 1)):
    if(respId in responders):
        return responders[respId]
    else:
        raise Exception("Responder not exist with given id " + str(respId))

@app.get("/responders/by-name")
def empByName(name: Optional[str] = None):
    if name == None:
        return {"message" : "no input provided"}
    for respId in responders:
        if responders[respId]["name"] == name:
            return responders[respId]
    return {"message" : "Not found"}

@app.post("/responders")
def createEmployee(resp: Responder):
    noOfResps = len(responders)
    newId = noOfResps + 1
    responders[newId] = resp
    return {"id" : newId, "name" : resp.name}
