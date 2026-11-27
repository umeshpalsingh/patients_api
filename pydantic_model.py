from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: str

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    address: Address
    

address_dict = {"city": "noida", "state": "uttar pradesh", "pin": "201301"} 

addess1 = Address(**address_dict)

patient_dict = {"name": "Umesh", "age": 25, "gender": "Male", "address": addess1}

patient1 = Patient(**patient_dict)

# print(patient1)
print(patient1.address.city)

temp = patient1.model_dump_json()

temp1 = patient1.model_dump(include=['name', 'age'])

temp2 = patient1.model_dump(exclude={'address':['state']})

print(temp)
print(type(temp))

print(temp1)

print(temp2)


