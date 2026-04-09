from pydantic import BaseModel,Field

class AskQuestion(BaseModel):
    question : str = Field(..., description="ask the questions")