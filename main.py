from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import engine, get_db
from schemas import EmployeeCreate, EmployeeResponse

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    description="A REST API to manage employee records",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Employee Management API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Create Employee
@app.post("/employees", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    existing_employee = db.query(models.Employee).filter(
        models.Employee.email == employee.email
    ).first()

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_employee = models.Employee(**employee.model_dump())

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee
# Get All Employees
@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()
    return employees
# Get Employee by ID
@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee
    return employee


# Update Employee
@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    existing_employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if existing_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    existing_employee.first_name = employee.first_name
    existing_employee.last_name = employee.last_name
    existing_employee.email = employee.email
    existing_employee.department = employee.department
    existing_employee.salary = employee.salary

    db.commit()
    db.refresh(existing_employee)

    return existing_employee