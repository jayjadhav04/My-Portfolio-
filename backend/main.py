import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from bson import ObjectId
from typing import List
from database import db
from models import Project, Skill, Certification, ContactMessage, AdminLogin, TokenResponse
from auth import verify_password, create_access_token, ADMIN_USER, get_current_user

app = FastAPI(title="Portfolio Admin API")

# Serve admin dashboard
app.mount("/admin", StaticFiles(directory="admin", html=True), name="admin")

# ---------- Public API ----------
@app.get("/api/projects", response_model=List[Project])
async def get_projects():
    projects = await db.projects.find().to_list(100)
    return projects

@app.get("/api/skills", response_model=List[Skill])
async def get_skills():
    skills = await db.skills.find().to_list(100)
    return skills

@app.get("/api/certifications", response_model=List[Certification])
async def get_certifications():
    certs = await db.certifications.find().to_list(100)
    return certs

@app.post("/api/contact")
async def submit_contact(message: ContactMessage):
    await db.messages.insert_one(message.dict())
    return {"status": "received"}

# ---------- Login ----------
@app.post("/api/login", response_model=TokenResponse)
async def login(login_data: AdminLogin):
    if login_data.username != ADMIN_USER["username"] or not verify_password(login_data.password, ADMIN_USER["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(data={"sub": login_data.username})
    return {"access_token": token, "token_type": "bearer"}

# ---------- Admin CRUD ----------
@app.post("/api/admin/projects")
async def add_project(project: Project, user: str = Depends(get_current_user)):
    result = await db.projects.insert_one(project.dict(exclude_unset=True))
    return {"id": str(result.inserted_id)}

@app.put("/api/admin/projects/{project_id}")
async def update_project(project_id: str, project: Project, user: str = Depends(get_current_user)):
    await db.projects.update_one({"_id": ObjectId(project_id)}, {"$set": project.dict(exclude_unset=True)})
    return {"status": "updated"}

@app.delete("/api/admin/projects/{project_id}")
async def delete_project(project_id: str, user: str = Depends(get_current_user)):
    await db.projects.delete_one({"_id": ObjectId(project_id)})
    return {"status": "deleted"}

@app.post("/api/admin/skills")
async def add_skill(skill: Skill, user: str = Depends(get_current_user)):
    result = await db.skills.insert_one(skill.dict())
    return {"id": str(result.inserted_id)}

@app.put("/api/admin/skills/{skill_id}")
async def update_skill(skill_id: str, skill: Skill, user: str = Depends(get_current_user)):
    await db.skills.update_one({"_id": ObjectId(skill_id)}, {"$set": skill.dict()})
    return {"status": "updated"}

@app.delete("/api/admin/skills/{skill_id}")
async def delete_skill(skill_id: str, user: str = Depends(get_current_user)):
    await db.skills.delete_one({"_id": ObjectId(skill_id)})
    return {"status": "deleted"}

@app.post("/api/admin/certifications")
async def add_cert(cert: Certification, user: str = Depends(get_current_user)):
    result = await db.certifications.insert_one(cert.dict())
    return {"id": str(result.inserted_id)}

@app.delete("/api/admin/certifications/{cert_id}")
async def delete_cert(cert_id: str, user: str = Depends(get_current_user)):
    await db.certifications.delete_one({"_id": ObjectId(cert_id)})
    return {"status": "deleted"}

@app.get("/api/admin/messages")
async def get_messages(user: str = Depends(get_current_user)):
    return await db.messages.find().to_list(100)

@app.get("/")
async def root():
    return {"message": "Portfolio API is running"}
