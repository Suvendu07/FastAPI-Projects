from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, status
import os
import uuid
from app.db.fake_db import jobs_db
from app.schemas.response import JobStatusResponse
from app.core.task import process_file




router = APIRouter()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok= True)




@router.get("/")
def home():
    return {"message":"API runs Successfuly"}



@router.post("/upload")
def upload_file(
    background_tasks : BackgroundTasks,
    file : UploadFile = File(...)
):
    
    jobs_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{jobs_id}_{file.filename}")
    
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        
        
    jobs_db[jobs_id] = {
        "status" : "pending",
        "result" : None,
        "filename" : file.filename
    }
    
    
    background_tasks.add_task(process_file, jobs_id,file_path)
    
    return {"job_id":jobs_id, "file_path":file_path}



@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id : str):
    
    job = jobs_db.get(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job not found")
    
    
    return {
        "job_id" : job_id,
        "status" : job["status"],
        "result" : job["result"]
    }
    

@router.get("/jobs")
def get_job_status():
    
    job = jobs_db
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job not found")
    
    
    return job
    
    
    
@router.delete("/jobs/{job_id}")
def delete_job(job_id: str):
    if job_id not in jobs_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job not found")
    
    
    jobs_db.pop(job_id)
    return {
        "message":"job deleted"
    }