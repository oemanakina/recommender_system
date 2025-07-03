# End-to-End Dual-Domain Recommender System

This project demonstrates the creation of an end-to-end machine learning pipeline, adaptable to multiple business domains. It currently implements a dual-recommender system for:
1.  **Language Learning:** Analyzes a student's test errors to recommend specific practice exercises.
2.  **Telecom Churn:** Predicts customer churn based on their account and usage data.

The project is designed to showcase best practices in data processing, model training, and project organization, aligning with the requirements for a modern AI/ML role.

---

## Project Structure

The repository is organized into a modular structure to ensure clarity and scalability:

```
.
├── artifacts/         # Stores output files like models and metrics (created after training)
├── data/
│   ├── processed/     # Stores cleaned, validated data (created after data loading)
│   ├── *.csv          # Raw input datasets
├── .docs/
│   ├── implementation_plan.md
│   ├── role.txt
├── legacy/            # Contains the original, single-file script for reference
├── notebooks/         # For exploratory data analysis (EDA) and experimentation
├── src/               # All source code for the project
│   ├── schemas/       # Machine-readable data validation schemas
│   ├── data_loader.py # Script for deterministic data ingestion and validation
│   ├── train.py       # Script for model training and evaluation
├── dashboard/         # (Future) Will contain the interactive Streamlit dashboard
├── requirements.txt   # Project dependencies
└── README.md          # This file
```

---

## Current Progress (Phase 5 Complete)

We have successfully implemented the first six phases of our development plan:

### ✅ Phase 0: Project Scaffolding
The project structure has been established, separating concerns like source code, data, and documentation. The original script has been moved to the `legacy` folder for historical reference.

### ✅ Phase 1: Deterministic Data Pipelines
A robust data ingestion pipeline has been created using `src/data_loader.py`. This script:
- Reads a raw CSV dataset.
- Validates its structure and values against a machine-readable schema defined in `src/schemas/`.
- Processes and saves the clean data in the efficient Parquet format under `data/processed/`.
- Generates a JSON log file to ensure reproducibility and track data provenance.

### ✅ Phase 2: Feature Engineering & Baseline Models
A flexible model training pipeline has been implemented in `src/train.py`. This script:
- Loads the processed data for a specified domain (language or telecom).
- Applies a domain-specific feature engineering pipeline.
- Trains a baseline classifier.
- Evaluates the model on a test set and saves the performance metrics and the trained model to the `artifacts/` directory.

### ✅ Phase 3: Rule-Based Recommendation Engine
A recommendation engine has been implemented in `src/recommend.py`. This script uses the trained models and business logic to translate raw predictions into actionable advice for both domains.

### ✅ Phase 4: Programmatic Interfaces (API & CLI)
The project's models and recommendation logic are now accessible through robust programmatic interfaces, including a REST API for real-time integration and an enhanced CLI for batch processing.

### ✅ Phase 5: Interactive Dashboard
An interactive web dashboard has been developed in `dashboard/app.py` using Streamlit. This provides a user-friendly interface for non-technical stakeholders to receive model-driven recommendations by communicating with the backend API.

---

## How to Run the Project

To get the project up and running and reproduce the results so far, follow these steps.

### 1. Setup Environment

First, create and activate a Python virtual environment.

```bash
# Create the environment (only needs to be done once)
python3 -m venv venv

# Activate the environment (needs to be done for each new terminal session)
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Next, install all the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the Data Pipeline

Execute the data loader script for both domains.

```bash
python src/data_loader.py language data/sample_score_new.csv
python src/data_loader.py telecom data/telecom_churn.csv
```

### 3. Run the Training Pipeline

Run the training script for both domains to create the model artifacts.

```bash
python src/train.py language
python src/train.py telecom
```

### 4. Run the Recommendation Engine (CLI)

The command-line interface can be used for single predictions or batch processing.

**Language Domain (Single Prediction):**
```bash
python src/recommend.py language data/sample_score_new.csv
```

**Telecom Domain (Batch Processing):**
```bash
python src/recommend.py telecom data/telecom_churn.csv
```

### 5. Run the API Server and Interactive Dashboard

To see the full application in action, you need to run two processes simultaneously in two separate terminals.

**In your first terminal, start the API server:**
```bash
# Make sure your virtual environment is active
uvicorn src.api:app --reload
```
The server will be running at `http://127.0.0.1:8000`. Leave this terminal open.

**In your second terminal, start the dashboard:**
```bash
# Make sure your virtual environment is active
streamlit run dashboard/app.py
```
Your web browser should open a new tab with the interactive dashboard.

---

## Next Steps

The final phase of the project will focus on packaging the project for presentation:
- **Phase 6:** Create final narrative artifacts, including a walkthrough notebook and presentation slides. 