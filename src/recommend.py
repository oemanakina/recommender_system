import argparse
import pandas as pd
import logging
import json
import joblib
from pathlib import Path
import csv

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Language Domain Logic (Refactored from legacy script) ---

# KEY for skill names from the original project
LEGEND = {"V": "Vocabulary", "A": "Word Agreement", "S": "Spelling", "Gen": "Gender", "Per": "Persons", "G": "Grammar", "T": "Tenses", "Past": "Past Tenses", "Fut": "Future Tenses", "M": "Modes", "Sub": "Subjunctive Mode", "Hyp": "Hypothetical Mode", "Pro": "Professional Communication", "Pron": "Pronouns", "Prep": "Prepositions"}
MISTAKES_PER_SKILL = [4, 1, 4, 2, 2, 11, 7, 3, 2, 3, 1, 1, 4, 2, 1]

def _analyze_language_errors(student_data_path):
    """Analyzes a student's score file to find their weakest skills."""
    student_mistakes = {key: 0 for key in LEGEND}
    skill_weights = {key: 0 for key in LEGEND}
    
    with open(student_data_path, "r") as f:
        reader = csv.reader(f)
        results = list(reader)

    # There are 20 questions in the test format
    for i in range(20):
        if results[i][0] == '2': continue  # Skip questions with full marks

        skill_list = results[i][1].split(",")
        if results[i][0] == '1':
            skill_list.pop(0)  # If score is 1, first skill is mastered, skip it

        for skill in skill_list:
            student_mistakes[skill] += 1

    ideal_set = []
    i = 0
    for key in student_mistakes:
        # Calculate a weight for the skill based on errors vs. total possible errors
        skill_weights[key] = student_mistakes[key] / MISTAKES_PER_SKILL[i]
        if skill_weights[key] >= 0.4:
            ideal_set.append(1)
        else:
            ideal_set.append(0)
        i += 1
        
    return ideal_set, skill_weights

def _find_best_exercises(ideal_set, exercises_path="data/exercises.csv"):
    """Finds the top 3 best matching exercises based on a student's weak skills."""
    with open(exercises_path, newline='') as csvfile:
        exercises = [list(map(int, row)) for row in csv.reader(csvfile)]
    
    matched = {}
    for i, exercise_vector in enumerate(exercises):
        # Count how many of the student's weak skills are covered by this exercise
        matches = sum(1 for j in range(len(ideal_set)) if ideal_set[j] == 1 and exercise_vector[j] == 1)
        matched[i] = matches

    # Sort exercises by the number of matches and take the top 3
    top_3_indices = sorted(matched, key=matched.get, reverse=True)[:3]
    return {index: exercises[index] for index in top_3_indices}

def recommend_language_exercises(student_data_path):
    """Generates a full recommendation report for the language learning domain."""
    ideal_set, skill_weights = _analyze_language_errors(student_data_path)
    
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

# --- Telecom Domain Logic ---

def recommend_telecom_retention(customer_data):
    """Generates a churn retention recommendation based on model prediction."""
    model_path = "artifacts/telecom_model.joblib"
    logging.info(f"Loading telecom model from {model_path}")
    pipeline = joblib.load(model_path)
    
    # Convert single customer dict to DataFrame for prediction
    df = pd.DataFrame([customer_data])
    
    # Get probability of churn (class 1)
    churn_prob = pipeline.predict_proba(df)[0][1]
    
    logging.info(f"Predicted churn probability: {churn_prob:.2f}")
    
    if churn_prob < 0.3:
        recommendation = "Low Risk: No action needed. Monitor quarterly."
    elif churn_prob < 0.7:
        recommendation = "Medium Risk: Offer a 10% loyalty discount or a small service upgrade."
    else:
        recommendation = "High Risk: Proactively contact customer with a personalized retention offer from a senior specialist."
        
    return f"Churn Probability: {churn_prob:.2%} - Recommendation: {recommendation}"

def main(domain, input_data):
    """Main recommendation function."""
    logging.info(f"Generating recommendation for domain: {domain}")
    
    if domain == "language":
        recommendation = recommend_language_exercises(input_data)
    elif domain == "telecom":
        # For CLI, we expect a JSON string as input
        try:
            customer_data = json.loads(input_data)
            recommendation = recommend_telecom_retention(customer_data)
        except json.JSONDecodeError:
            logging.error("Invalid JSON string for telecom customer data.")
            recommendation = "Error: Input must be a valid JSON string for the telecom domain."
    else:
        raise ValueError("Invalid domain specified.")
        
    print("\n--- Recommendation Report ---")
    print(recommendation)
    print("---------------------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recommendation Engine CLI")
    parser.add_argument("domain", choices=["language", "telecom"], help="The domain to generate a recommendation for.")
    parser.add_argument("input", type=str, help="Input for the recommendation. For 'language', this is a file path to a student's scores. For 'telecom', this is a JSON string of customer data.")
    
    args = parser.parse_args()
    main(args.domain, args.input) 