import pandas as pd
import logging
from fastapi import FastAPI
from pydantic import BaseModel, Field
from io import StringIO
import csv
import joblib

# Import recommendation logic from our existing script
from src.recommend import recommend_telecom_retention, recommend_language_exercises

# Setup basic logging and App
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = FastAPI()

# --- Pydantic Models for Request Body Validation ---

class TelecomCustomer(BaseModel):
    gender: str
    SeniorCitizen: int = Field(..., alias='SeniorCitizen')
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MonthlyCharges: float
    TotalCharges: float

class LanguageInput(BaseModel):
    score_file_content: str

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Prediction and Recommendation API"}

@app.post("/predict/telecom")
def predict_churn(customer: TelecomCustomer):
    """Predicts churn and provides a retention recommendation for a single customer."""
    logging.info("Received request for telecom prediction")
    # Pydantic's `dict()` with `by_alias=True` handles the alias for SeniorCitizen
    recommendation = recommend_telecom_retention(customer.dict(by_alias=True))
    return {"recommendation": recommendation}

@app.post("/predict/language")
def predict_language(input_data: LanguageInput):
    """Analyzes student score data (as a string) and recommends exercises."""
    logging.info("Received request for language prediction")
    
    # Use StringIO to treat the string content as a file-like object
    f = StringIO(input_data.score_file_content)
    reader = csv.reader(f)
    score_rows = list(reader)
    
    recommendation = recommend_language_exercises(score_rows)
    return {"recommendation": recommendation}

# To run this API:
# uvicorn src.api:app --reload 