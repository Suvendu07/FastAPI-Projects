from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
import pickle
from fastapi.responses import JSONResponse
import pandas as pd
from schema.user_input import UserInput
from models.predict import MODEL_VERSION, model, predict_output
from schema.prediction_response import PredictionResponse

    
app = FastAPI()



"""now you are saying that if there is already a HOME endpoint why we create a another endpoint health. the home endpoint is only for human readable while health endpoint is machine readable."""
# Human Readable
@app.get('/')
def home():
    return {'message':'insurance premium prediction API'}


# Machine Readable
"""When we deploy AWS cloud platfrom and wahne pe agar koi kubbernate or elastic load balancer jese service use karte ho AWS ki wo app ko force karata he ek health check endpoint add karo. it helps the AWS to say that the API is live now."""
@app.get('/health')
def health_check():
    return {
        'status':'ok',
        'version':MODEL_VERSION,
        'model_loaded' : model is not None
    }


@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }
    
    try:
        
      prediction = predict_output(user_input)

      return JSONResponse(status_code=200, content={'predicted_category': prediction})
  
    except Exception as e:
        
       return  JSONResponse(status_code=500, content=str(e))
