import argparse
import yaml
import pandas as pd
import hashlib
import json
import logging
from pathlib import Path

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_schema(schema_path):
    """Loads a YAML schema file."""
    logging.info(f"Loading schema from: {schema_path}")
    with open(schema_path, 'r') as f:
        return yaml.safe_load(f)

def validate_data(df, schema):
    """Validates a DataFrame against a schema."""
    logging.info("Starting data validation...")
    # Simplified validation logic for demonstration
    # A robust solution would have more complex checks
    for col_schema in schema['columns']:
        col_name = col_schema['name']
        if col_name not in df.columns:
            raise ValueError(f"Missing required column: {col_name}")
    logging.info("Data validation successful.")
    return True

def hash_file(file_path):
    """Computes the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def main(domain, input_path, output_dir):
    """Main data loading, validation, and processing function."""
    input_file = Path(input_path)
    output_path = Path(output_dir)
    
    if not input_file.exists():
        logging.error(f"Input file not found: {input_file}")
        raise FileNotFoundError(f"Input file not found: {input_file}")

    output_path.mkdir(parents=True, exist_ok=True)

    schema_path = Path(f"src/schemas/{domain}_schema.yml")
    if not schema_path.exists():
        logging.error(f"Schema not found for domain: {domain}")
        raise FileNotFoundError(f"Schema not found for domain: {domain}")

    schema = load_schema(schema_path)

    # Read data
    logging.info(f"Reading data from: {input_file}")
    df = pd.read_csv(input_file, delimiter=schema.get('delimiter', ','))

    # Perform validation
    validate_data(df, schema)

    # Define output file paths
    processed_file = output_path / f"{domain}_processed.parquet"
    log_file = output_path / f"{domain}_log.json"

    # Save processed data
    logging.info(f"Saving processed data to: {processed_file}")
    df.to_parquet(processed_file, index=False)

    # Create and save log
    log_data = {
        'input_file': str(input_file),
        'input_hash': hash_file(input_file),
        'processed_file': str(processed_file),
        'row_count': len(df),
        'schema': str(schema_path)
    }
    logging.info(f"Saving log file to: {log_file}")
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=4)

    logging.info("Data processing complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Ingestion and Validation CLI")
    parser.add_argument("domain", choices=["language", "telecom"], help="The data domain to process.")
    parser.add_argument("input_path", type=str, help="Path to the raw input CSV file.")
    parser.add_argument("--output_dir", type=str, default="data/processed", help="Directory to save processed data and logs.")
    
    args = parser.parse_args()
    
    main(args.domain, args.input_path, args.output_dir) 