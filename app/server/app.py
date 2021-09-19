from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse
import json
import pymongo

myclient = pymongo.MongoClient("mongodb+srv://bigd:r%26kkGK%218mjX2rG@cluster0.vapic.mongodb.net/admin?retryWrites=true&w=majority")
print(myclient.test)
db = myclient["organchaintest"]

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age = 3600
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


@app.get('/donors')
async def list_donors():
    donors = []
    for donor in db.donors.find({},{"_id": 0}):
        donors.append(donor)
    print(donors)
    return {'donors': donors}


@app.post('/donors', response_description="donor data added into the database")
async def add_donor_data(donor_details):
    decoded_details = urllib.parse.unquote(donor_details)
    decoded_details = json.loads(decoded_details)
    donor_details_json = jsonable_encoder(decoded_details)
    insert = db.donors.insert_one(donor_details_json)
    return "Donor added successfully."

@app.get('/patients')
async def list_donors():
    patients = []
    for patient in db.patients.find({},{"_id": 0}):
        patients.append(patient)
    print(patients)
    return {'patient': patients}


@app.post('/patients', response_description="patient data added into the database")
async def add_patient_data(patient_details):
    decoded_details = urllib.parse.unquote(patient_details)
    decoded_details = json.loads(decoded_details)
    donor_details_json = jsonable_encoder(decoded_details)
    insert = db.patients.insert_one(donor_details_json)
    return "patient added successfully."


@app.get('/match')
async def find_matches():
    for donor in db.donors.find({},{"_id": 0}):
        donor_name = donor.get('name')
        donor_organ = donor.get('organ')
        donor_bloodtype = donor.get("bloodtype")
        for patient in db.patients.find({}, {"_id": 0}):
            patient_name = patient.get("name")
            patient_organ = patient.get('organ')
            patient_bloodtype = patient.get('bloodtype')
            if donor_organ == patient_organ and donor_bloodtype == patient_bloodtype:
                #matched!
                matched_pair = [donor, patient]
                return {"matched_pair": matched_pair}
    return {"matched_pair": []}
     




