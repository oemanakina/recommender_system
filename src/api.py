import pandas as pd
import logging
from fastapi import FastAPI
from pydantic import BaseModel, Field
from io import StringIO
import csv
import joblib

# Import recommendation logic from our existing script
from src.recommend import recommend_telecom_retention, _analyze_language_errors, _find_best_exercises, LEGEND

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

def recommend_language_exercises_from_content(score_file_content: str):
    """Generates a full recommendation report for the language learning domain from string content."""
    # Use StringIO to treat the string content as a file
    f = StringIO(score_file_content)
    reader = csv.reader(f)
    # Re-use the core logic, but with in-memory data instead of a file path
    ideal_set, skill_weights = _analyze_language_errors(list(reader))
    
    skills_to_practice = [key for key, value in skill_weights.items() if value >= 0.4]

    if not skills_to_practice:
        return "Excellent work! No specific weaknesses found based on this test."

    text = "Based on your results, you should focus on the following areas:\n"
    for skill_key in skills_to_practice:
        text += f"- {LEGEND[skill_key]}\n"
    
    best_exercises = _find_best_exercises(ideal_set)
    text += "\nWe recommend the following practice sets:\n"
    for exercise_id, vector in best_exercises.items():
        text += f"\n- Exercise Set {exercise_id + 1}:\n"
        text += "  Focuses on: "
        covered_skills = [LEGEND[key] for i, key in enumerate(LEGEND) if vector[i] == 1]
        text += ", ".join(covered_skills) + "."
        
    return text

@app.post("/predict/language")
def predict_language(input_data: LanguageInput):
    """Analyzes student score data (as a string) and recommends exercises."""
    logging.info("Received request for language prediction")
    recommendation = recommend_language_exercises_from_content(input_data.score_file_content)
    return {"recommendation": recommendation}

# To run this API:
# uvicorn src.api:app --reload 