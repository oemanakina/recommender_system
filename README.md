# End-to-End Dual-Domain Recommender System

This project is an end-to-end Machine Learning system built to demonstrate the complete lifecycle of developing and deploying a predictive model. The primary use case focuses on **predicting telecom customer churn**, a classic and high-value business problem.

To showcase architectural flexibility, the same end-to-end principles are also applied to a secondary, unique domain: recommending exercises for language learners.

Built entirely in **Python**, the project leverages core **data analysis libraries** like **pandas** for data manipulation and **scikit-learn** for its feature engineering and modeling pipelines. The system provides a practical, hands-on application of fundamental **machine learning concepts and algorithms**, covering the full lifecycle from data ingestion and validation to model deployment via an interactive dashboard and a REST API.

---

### Project Background & Evolution

This project is a significant expansion and modernization of an original concept developed for the "Intro to AI" course (COMP3106) in the Computer Science department at Carleton University during the Fall 2022 semester.

The initial project, created by Olga Manakina and Suchanya Limpakom, was a recommender system designed to generate a personalized learning path for French language students. It analyzed a user's score on a custom-designed test—which evaluated specific skills like grammar, vocabulary, and tenses—to predict their chances of achieving a certain proficiency level. Based on the results, it would then recommend specific exercise sets to address the student's weaknesses.

This version of the project preserves that core idea but refactors it into a robust, end-to-end ML pipeline and demonstrates its adaptability by applying the same architectural principles to a new, industry-standard telecom churn problem.

The original code and a more detailed description of the initial project can be found in the `legacy/` folder for historical context.

---

## Key Features

The system is built with a modular, professional structure, incorporating the following features:

*   **Validated Data Pipelines:** Raw data for each domain is processed through a deterministic pipeline that validates it against a pre-defined schema, ensuring data quality and reproducibility.
*   **Modular Model Training:** Uses `scikit-learn` Pipelines to cleanly encapsulate feature engineering (e.g., `StandardScaler`, `OneHotEncoder`) and model training (`LogisticRegression` for churn). This creates reusable and easily understandable model artifacts.
*   **Actionable Recommendation Engine:** A rule-based system translates the raw probabilistic outputs of the models into clear, human-readable business recommendations (e.g., churn risk categories, personalized study plans).
*   **REST API for Real-Time Predictions:** A `FastAPI` server exposes the prediction logic through web endpoints, allowing for easy integration with other applications and services.
*   **Interactive Dashboard:** A user-friendly web application built with `Streamlit` provides a front-end for non-technical users to interact with the models, input data, and visualize results.
*   **Batch Processing CLI:** The system includes a command-line interface capable of processing large CSV files of customers at once, generating recommendations for each.

---

## Running the Application

There are three ways to interact with this project: through the Command-Line Interface (CLI), the Interactive Dashboard, or the API.

### 1. Initial Setup (Required for all methods)

First, create the environment and install dependencies:
```bash
# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
Next, run the data processing and model training scripts to generate the required artifacts:
```bash
# Process data
python src/data_loader.py telecom data/telecom_churn.csv
python src/data_loader.py language data/sample_score_new.csv

# Train models
python src/train.py telecom
python src/train.py language
```

### 2. Using the Interactive Dashboard (Recommended)

The dashboard is the easiest way to interact with the project. You must run the API server and the dashboard app simultaneously in two separate terminals.

**Terminal 1: Start the API Server**
```bash
uvicorn src.api:app --reload
```
**Terminal 2: Start the Dashboard**
```bash
streamlit run dashboard/app.py
```
A new tab will open in your browser with the dashboard.

### 3. Using the Command-Line Interface

The CLI is useful for batch processing or single predictions.

**Telecom Domain (Batch Processing):**
```bash
python src/recommend.py telecom data/telecom_churn.csv
```
**Language Domain (Single Prediction):**
```bash
python src/recommend.py language data/sample_score_new.csv
```
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
├── dashboard/         # Contains the interactive Streamlit dashboard
├── requirements.txt   # Project dependencies
└── README.md          # This file
```

---

## Datasets Used

This project utilizes two distinct datasets to showcase the adaptability of the pipeline.

**1. Telecom Customer Churn**
*   **Source:** [IBM Sample Datasets / Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
*   **Description:** A classic dataset containing information about 7,043 fictional telecom customers and their account details, services, and whether they churned in the last quarter.
*   **Reason for Choice:** This is a standard benchmark for customer churn prediction and directly aligns the project with the telecom industry use case, making it relevant for roles in that sector.

**2. French Language Learner Errors**
*   **Source:** Original project data.
*   **Description:** A custom dataset representing a student's scores on a 20-question French language test, mapping errors to specific linguistic skills.
*   **Reason for Choice:** This was the initial dataset for the project. It serves to demonstrate the ability to refactor legacy code and shows how the core pipeline can be generalized from a niche educational problem to a common business problem. 