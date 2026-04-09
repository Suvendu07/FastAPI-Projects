from pydantic import BaseModel, Field

class GiveResponse(BaseModel):
    answers : str = Field(..., description="llm give the response")