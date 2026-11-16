from pydantic import BaseModel, EmailStr, ConfigDict


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    salary: int


class EmployeeResponse(EmployeeCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)