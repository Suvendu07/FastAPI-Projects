from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal
from config.city_tier import tier_1_cities, tier_2_cities


# pydantic model to validate incoming data
class UserInput(BaseModel):
           
    age : Annotated[int, Field(..., gt = 0, lt = 128, description='age of the user')]
    weight :Annotated[float, Field(..., gt = 0, lt=120, description='weigth of the user')]
    height : Annotated[float, Field(..., gt = 0, lt = 2.5, description='height of the user')]
    income_lpa: Annotated[float, Field(..., gt = 0, description='annual salary of the user in lpa')]
    smoker: Annotated[bool, Field(..., description='Is user a smoker')]
    city: Annotated[str, Field(..., description='The city that the user belongs to')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]
    
    
    
    """This field is use for if a user enter a city name capital so the ml model will be hallucinate and give bad response so to solve this validate the city.now if the user enter in capital or samll it treat like a one word."""
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v:str) -> str:
        V = v.strip().title()
        return v
    
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3