import time
from app.db.fake_db import jobs_db


def process_file(job_id : str, file_path : str):
    jobs_db[job_id]['status'] = "processing"
    
    time.sleep(5)
    
    
    jobs_db[job_id]["status"] = "completed"
    jobs_db[job_id]['result'] = f"Processed file at {file_path}"