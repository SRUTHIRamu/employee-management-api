from fastapi import FastAPI

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