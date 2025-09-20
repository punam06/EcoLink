# Simple Mock Backend API for EcoLink
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from typing import List, Optional
import uuid
from datetime import datetime

app = FastAPI(title="EcoLink Mock API", description="Mock backend for EcoLink demo")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ecolink-demo.surge.sh", "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access: str
    refresh: str
    user: dict

class RegisterRequest(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    password: str

class FileUpload(BaseModel):
    filename: str
    size: int
    content_type: str

# Mock database
mock_users = {
    "demo": {"username": "demo", "password": "demo123", "email": "demo@ecolink.com"},
    "admin": {"username": "admin", "password": "admin123", "email": "admin@ecolink.com"}
}

mock_files = []
mock_analytics = {
    "total_files": 45,
    "total_size_gb": 12.3,
    "co2_saved": 234.5,
    "energy_saved": 45.2,
    "duplicates_found": 8
}

@app.get("/")
async def root():
    return {"message": "EcoLink Mock API is running!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/auth/login/", response_model=LoginResponse)
async def login(request: LoginRequest):
    if request.username in mock_users and mock_users[request.username]["password"] == request.password:
        return LoginResponse(
            access=f"mock-access-token-{request.username}",
            refresh=f"mock-refresh-token-{request.username}",
            user={"username": request.username, "email": mock_users[request.username]["email"]}
        )
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/register/")
async def register(request: RegisterRequest):
    if request.username in mock_users:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    mock_users[request.username] = {
        "username": request.username,
        "password": request.password,
        "email": request.email,
        "firstName": request.firstName,
        "lastName": request.lastName
    }
    
    return {"message": "User registered successfully", "username": request.username}

@app.get("/api/v1/analytics/summary/")
async def get_analytics():
    return {
        "data": mock_analytics,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/files/")
async def get_files():
    return {
        "results": [
            {
                "id": 1,
                "filename": "document.pdf",
                "size": 1048576,
                "upload_date": "2024-09-20T10:30:00Z",
                "co2_impact": 0.45,
                "is_duplicate": False
            },
            {
                "id": 2,
                "filename": "image.jpg",
                "size": 2097152,
                "upload_date": "2024-09-20T11:15:00Z",
                "co2_impact": 0.89,
                "is_duplicate": False
            },
            {
                "id": 3,
                "filename": "spreadsheet.xlsx",
                "size": 524288,
                "upload_date": "2024-09-20T14:22:00Z",
                "co2_impact": 0.22,
                "is_duplicate": True
            }
        ],
        "count": 3
    }

@app.post("/api/v1/files/request-upload-url/")
async def request_upload_url(file: FileUpload):
    return {
        "upload_url": f"https://mock-storage.com/upload/{uuid.uuid4()}",
        "file_id": str(uuid.uuid4()),
        "expires_in": 3600
    }

@app.post("/api/v1/files/commit/")
async def commit_file_upload(file_data: dict):
    new_file = {
        "id": len(mock_files) + 1,
        "filename": file_data.get("filename", "unknown"),
        "size": file_data.get("size", 0),
        "upload_date": datetime.now().isoformat(),
        "co2_impact": round(file_data.get("size", 0) * 0.0000004, 2),
        "is_duplicate": False
    }
    mock_files.append(new_file)
    return {"message": "File uploaded successfully", "file": new_file}

@app.get("/api/v1/analytics/file-types/")
async def get_file_types():
    return {
        "data": [
            {"type": "PDF", "count": 15, "size_gb": 4.2},
            {"type": "Images", "count": 20, "size_gb": 6.8},
            {"type": "Documents", "count": 8, "size_gb": 1.1},
            {"type": "Videos", "count": 2, "size_gb": 0.2}
        ]
    }

@app.get("/api/v1/analytics/impact-trend/")
async def get_impact_trend():
    return {
        "data": [
            {"date": "2024-09-15", "co2_saved": 45.2, "files": 8},
            {"date": "2024-09-16", "co2_saved": 67.8, "files": 12},
            {"date": "2024-09-17", "co2_saved": 89.1, "files": 15},
            {"date": "2024-09-18", "co2_saved": 123.4, "files": 22},
            {"date": "2024-09-19", "co2_saved": 178.9, "files": 35},
            {"date": "2024-09-20", "co2_saved": 234.5, "files": 45}
        ]
    }

@app.get("/api/v1/recommendations/")
async def get_recommendations():
    return {
        "results": [
            {
                "type": "duplicate",
                "title": "Remove duplicate files",
                "description": "You have 8 duplicate files taking up 2.3 GB of storage",
                "potential_savings": "1.2 kg CO2",
                "priority": "high"
            },
            {
                "type": "compression",
                "title": "Compress large images",
                "description": "12 images can be compressed to save space",
                "potential_savings": "0.8 kg CO2",
                "priority": "medium"
            },
            {
                "type": "archive",
                "title": "Archive old files",
                "description": "Files older than 6 months can be archived",
                "potential_savings": "0.5 kg CO2",
                "priority": "low"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)