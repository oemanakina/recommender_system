import argparse
import pandas as pd
import logging
import json
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def build_telecom_pipeline():
    """Builds the feature engineering and modeling pipeline for the telecom domain."""
    numeric_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    categorical_features = ['gender', 'Partner', 'Dependents', 'PhoneService']
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    return Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', LogisticRegression(solver='liblinear'))])

def build_language_pipeline():
    """Builds the feature engineering and modeling pipeline for the language domain."""
    return Pipeline(steps=[('tfidf', TfidfVectorizer()),
                           ('classifier', MultinomialNB())])

def main(domain):
    """Main model training and evaluation function."""
    logging.info(f"Starting training for domain: {domain}")
    
    # Define paths
    processed_data_path = Path(f"data/processed/{domain}_processed.parquet")
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    
    # Load data
    logging.info(f"Loading data from {processed_data_path}")
    df = pd.read_parquet(processed_data_path)
    
    if domain == "telecom":
        # Prepare data
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        X = df.drop('Churn', axis=1)
        y = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
        pipeline = build_telecom_pipeline()
        
    elif domain == "language":
        # Prepare data - ignore summary rows at the end if they exist
        if 'POINTS' in df['skills'].iloc[-2]:
             df = df.iloc[:-2].copy()
        
        X = df['skills']
        y = df['score'].astype(int)
        pipeline = build_language_pipeline()
        
    else:
        raise ValueError("Invalid domain specified.")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y if domain == 'telecom' else None)
    
    # Train model
    logging.info("Training model pipeline...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate model
    logging.info("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    
    avg_method = 'binary' if domain == 'telecom' else 'weighted'
    precision = precision_score(y_test, y_pred, average=avg_method)
    recall = recall_score(y_test, y_pred, average=avg_method)
    f1 = f1_score(y_test, y_pred, average=avg_method)
    cm = confusion_matrix(y_test, y_pred)
    
    metrics = {
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm.tolist()
    }
    
    logging.info(f"Metrics: {metrics}")
    
    # Save artifacts
    model_path = artifacts_dir / f"{domain}_model.joblib"
    metrics_path = artifacts_dir / f"{domain}_metrics.json"
    
    joblib.dump(pipeline, model_path)
    logging.info(f"Saved model pipeline to {model_path}")
    
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    logging.info(f"Saved metrics to {metrics_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Model Training CLI")
    parser.add_argument("domain", choices=["language", "telecom"], help="The domain to train a model for.")
    args = parser.parse_args()
    main(args.domain) 