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

## Current Progress (Phase 2 Complete)

We have successfully implemented the first three phases of our development plan:

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
- Applies a domain-specific feature engineering pipeline:
    - **Language:** `TfidfVectorizer` for text-based skills.
    - **Telecom:** `ColumnTransformer` to handle both numerical and categorical features.
- Trains a baseline classifier:
    - **Language:** `MultinomialNB`.
    - **Telecom:** `LogisticRegression`.
- Evaluates the model on a test set and saves the performance metrics (Precision, Recall, F1) to a JSON file.
- Saves the entire trained model pipeline as a `.joblib` file in the `artifacts/` directory.

---

## How to Run the Project

To get the project up and running and reproduce the results so far, follow these steps.

### 1. Setup Environment

First, clone the repository and set up a Python virtual environment.

```bash
# It is recommended to use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Next, install all the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the Data Pipeline (Phase 1)

Execute the data loader script for both the language and telecom domains. This will validate the raw data and create the processed Parquet files in `data/processed/`.

```bash
# Process the language data
python src/data_loader.py language data/sample_score_new.csv

# Process the telecom data
python src/data_loader.py telecom data/telecom_churn.csv
```

### 3. Run the Training Pipeline (Phase 2)

Now, run the training script for both domains. This will create the `artifacts/` directory and populate it with the trained models and their performance metrics.

```bash
# Train the language model
python src/train.py language

# Train the telecom model
python src/train.py telecom
```

After running these commands, you will have a fully trained model and all associated metrics for both domains, ready for the next phase of development.

---

## Next Steps

The next phases of the project will focus on building on top of these trained models:
- **Phase 3:** Implement a rule-based engine to translate model predictions into actionable recommendations.
- **Phase 4:** Expose the models via a REST API and a batch-processing CLI.
- **Phase 5 & 6:** Build an interactive dashboard and create final presentation artifacts. 