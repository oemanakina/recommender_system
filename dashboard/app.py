import streamlit as st
import pandas as pd
import altair as alt
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- App Configuration ---
st.set_page_config(
    page_title="Dual-Domain Recommender",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- API Communication ---
# Base URL for the local API server
API_BASE_URL = "http://127.0.0.1:8000"

def get_telecom_recommendation(customer_data):
    """Sends customer data to the API and gets a recommendation."""
    try:
        response = requests.post(f"{API_BASE_URL}/predict/telecom", json=customer_data)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()['recommendation']
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return f"Error: Could not connect to the recommendation API. Is the server running?"

def get_language_recommendation(score_file_content):
    """Sends score file content to the API and gets a recommendation."""
    try:
        payload = {"score_file_content": score_file_content}
        response = requests.post(f"{API_BASE_URL}/predict/language", json=payload)
        response.raise_for_status()
        return response.json()['recommendation']
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return f"Error: Could not connect to the recommendation API. Is the server running?"

# --- UI Components ---

def telecom_ui():
    """Renders the UI for the telecom churn prediction."""
    st.header("Telecom Customer Churn")
    st.write("Enter the customer's details below to predict their churn risk.")

    with st.form("telecom_form"):
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
            Partner = st.radio("Has Partner?", ["Yes", "No"])
            Dependents = st.radio("Has Dependents?", ["Yes", "No"])
            PhoneService = st.selectbox("Phone Service?", ["Yes", "No"])
        with col2:
            SeniorCitizen = st.selectbox("Is Senior Citizen?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
            tenure = st.slider("Tenure (Months)", 0, 72, 1)
            MonthlyCharges = st.number_input("Monthly Charges ($)", min_value=0.0, value=70.0, step=1.0)
            TotalCharges = st.number_input("Total Charges ($)", min_value=0.0, value=float(tenure * MonthlyCharges), step=1.0)
            
        submitted = st.form_submit_button("Get Recommendation")

    if submitted:
        customer_data = {
            "gender": gender, "SeniorCitizen": SeniorCitizen, "Partner": Partner,
            "Dependents": Dependents, "tenure": tenure, "PhoneService": PhoneService,
            "MonthlyCharges": MonthlyCharges, "TotalCharges": TotalCharges,
        }
        with st.spinner("Analyzing customer data..."):
            recommendation = get_telecom_recommendation(customer_data)
            st.success("Analysis Complete!")
            st.write(recommendation)

def language_ui():
    """Renders the UI for the language exercise recommendation."""
    st.header("Language Exercise Recommender")
    st.write("Paste the contents of the student's score CSV file below.")
    
    score_content = st.text_area("Score File Content", height=250, placeholder="1,\"V,A\"\n2,\"V,S\"\n...")
    
    if st.button("Get Recommendation"):
        if score_content:
            with st.spinner("Analyzing score data..."):
                recommendation = get_language_recommendation(score_content)
                st.success("Analysis Complete!")
                st.text_area("Recommended Focus and Exercises", recommendation, height=300)
        else:
            st.warning("Please paste some score content before proceeding.")


# --- Main App ---
st.title("Intelligent Recommendation System")

st.sidebar.title("Navigation")
domain = st.sidebar.radio("Choose a Domain", ["Telecom Churn", "Language Learning"])

if domain == "Telecom Churn":
    telecom_ui()
else:
    language_ui() 