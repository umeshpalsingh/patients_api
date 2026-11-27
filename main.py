from fastapi import FastAPI, Path, HTTPException, Query
import json 
from fastapi.responses import JSONResponse

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated, Literal

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Id of the patient", examples=['P001'])]
    name: Annotated[str, Field(max_length=20, title="Name of the patient", description="Give the name of the patient in less than 10 characters")]
    city: Annotated[str, Field(..., description="City where the patient is living ")]
    age: int = Field(ge=0, le=80)
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    weight: Annotated[float, Field(..., gt=0, description="weight of the patient in kgs")]
    height: Annotated[float, Field(..., gt=0, description="height of the patient in mtrs")]
    # allergies: Optional[List[str]] = None
    # contact_details: Dict[str, str]
    
    @computed_field
    @property
    def bmi(self) -> float: 
        bmi = round(self.weight / (self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
   
    
    
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    
    
# def update_patient_data(patient: Patient):
    
#     print(patient.name)
#     print(patient.age)
#     print(patient.married)
#     print(patient.weight)
#     print(patient.allergies)
#     print(patient.contact_details)


# patient_info = {"name": "Umesh", "age": 65, "height": "1.8", "weight": 75.2, "contact_details": {"phone": "+91-32343243", "emergency": "8737382378"}}

# patient1 = Patient(**patient_info)

# update_patient_data(patient1)



app = FastAPI()

def load_data():
    try:
        with open('patients.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open('patients.json', "w") as f:
        json.dump(data, f)


@app.get("/")
def home():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}

@app.get("/view")
def view():
    data = load_data()

    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the patient in the DB", example="P001")):

    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")

@app.get("/sort")
def sort_patients(sortby: str = Query(..., description="sort on the basis of height, weight or bmi"), order: str = Query('asc', description="sort in asc or desc order")):

    valid_fields = ["height", "weight", "bmi"]

    if sortby not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid field select between asc and desc')

    data = load_data()

    

@app.post("/create")
def create_patient(patient: Patient):
     
     # load existing data
     data = load_data()
     
     # check if the patient is already exists
     if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
     
     # new patient add to the database
     data[patient.id] = patient.model_dump(exclude=['id'])
     
     # save into the json file  
     save_data(data)
     
     return  JSONResponse(status_code=201, content={'message': "patient created successfully"})
 
 
 
@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_data = data[patient_id]
    
    print(existing_patient_data)
    
    updated_patient_data = patient_update.model_dump(exclude_unset=True)
    
    for key, value in updated_patient_data.items():
        existing_patient_data[key] = value
        
    existing_patient_data['id'] = patient_id
    # existing_patient_data -> pydantic object
    patient_pydantic_object = Patient(**existing_patient_data) #updated bmi + verdict
    # pydantic object -> dict
    existing_patient_data = patient_pydantic_object.model_dump(exclude='id')
        
    data[patient_id] = existing_patient_data
    
    save_data(data)
    
    return JSONResponse(status_code=200, content={"message": 'Patient updated successfully'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    
    #load data
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(status_code=200, content={"message": "Patient deleted"}) 
