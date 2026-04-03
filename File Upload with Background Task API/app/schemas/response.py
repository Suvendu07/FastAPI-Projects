from pydantic import BaseModel

class JobStatusResponse(BaseModel):
    job_id : str
    status : str
    result : str | None = None