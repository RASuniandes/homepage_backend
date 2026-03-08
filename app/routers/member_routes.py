from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.dependencies import get_db
from app.models.member import Member
from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
import uuid
import os
import json
from pathlib import Path
from app.config import get_settings
member_router = APIRouter(tags=["members"])

# Configure upload directory
UPLOAD_DIR = Path("uploads/members")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Admin password (consider using environment variables)
ADMIN_PASSWORD = get_settings().ADMIN_PASSWORD
class MemberBase(BaseModel):
  name: str
  email: EmailStr
  role: Optional[str] = None
  major: str
  double_major: Optional[str] = None
  u_code: Optional[str] = None
  phone_number: Optional[str] = None
  project: Optional[str] = None
  photo: Optional[str] = None
  contributions: Optional[List[str]] = None
  skills: Optional[List[str]] = None
  goals: Optional[List[str]] = None
  is_in_council: bool = False
  join_date: datetime

class MemberResponse(MemberBase):
  id: str
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True

class AdminAuthRequest(BaseModel):
  password: str

# Routes
@member_router.post("/request-join", response_model=MemberResponse)
async def request_join_member(
  name: str = Form(...),
  email: str = Form(...),
  major: str = Form(...),
  double_major: str = Form(default=""),
  u_code: str = Form(default=""),
  phone_number: str = Form(default=""),
  role: str = Form(default=""),
  project: str = Form(default=""),
  skills: str = Form(default="[]"),
  contributions: str = Form(default="[]"),
  goals: str = Form(default="[]"),
  photo: Optional[UploadFile] = File(None),
  db: Session = Depends(get_db)
):
  photo_path = None
  
  if photo:
    file_ext = Path(photo.filename).suffix
    unique_name = f"{uuid.uuid4()}{file_ext}"
    photo_path = UPLOAD_DIR / unique_name
    
    with open(photo_path, "wb") as f:
      f.write(await photo.read())
    
    photo_path = f"uploads/members/{unique_name}"

  db_member = Member(
    id=str(uuid.uuid4()),
    name=name,
    email=email,
    major=major,
    double_major=double_major or None,
    u_code=u_code or None,
    phone_number=phone_number or None,
    role=role or None,
    project=project or None,
    photo=photo_path,
    skills=json.loads(skills) if skills else None,
    contributions=json.loads(contributions) if contributions else None,
    goals=json.loads(goals) if goals else None,
    join_date=datetime.utcnow(),
    is_accepted=False,
  )
  
  db.add(db_member)
  db.commit()
  db.refresh(db_member)
  return db_member

@member_router.get("", response_model=List[MemberResponse])
async def get_members(
  skip: int = Query(0, ge=0),
  limit: int = Query(10, ge=1, le=100),
  db: Session = Depends(get_db)
):
  return db.query(Member).filter(Member.is_accepted == True).offset(skip).limit(limit).all()

@member_router.get("/to_add")
async def get_members_to_add(db: Session = Depends(get_db)):
  return db.query(Member).filter(Member.is_accepted == False).all()

@member_router.get("/{member_id}", response_model=MemberResponse)
async def get_member(member_id: str, db: Session = Depends(get_db)):
  member = db.query(Member).filter(Member.id == member_id).first()
  if not member:
    raise HTTPException(status_code=404, detail="Member not found")
  return member


@member_router.post("/authorize", response_model=dict)
async def authorize_admin(
  auth: AdminAuthRequest,
  db: Session = Depends(get_db)
):
  if auth.password != ADMIN_PASSWORD:
    raise HTTPException(status_code=401, detail="Incorrect password")
  return {"message": "Authorization successful"}

@member_router.post("/{member_id}/approve", response_model=MemberResponse)
async def approve_member(
  member_id: str,
  db: Session = Depends(get_db)
):
  member = db.query(Member).filter(Member.id == member_id).first()
  if not member:
    raise HTTPException(status_code=404, detail="Member not found")
  
  member.is_accepted = True
  db.commit()
  db.refresh(member)
  return member