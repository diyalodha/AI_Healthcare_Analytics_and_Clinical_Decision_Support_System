"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_ai_models.py

Purpose :
Generate AI Models Reference Dataset

Output :
reference_ai_models.csv

Author : Diya Lodha & Team
===========================================================
"""

import os
import sys
import pandas as pd


# ==========================================================
# Add Parent Directory
# ==========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PARENT_DIR = os.path.dirname(
    CURRENT_DIR
)

if PARENT_DIR not in sys.path:
    sys.path.insert(
        0,
        PARENT_DIR
    )

import config


# ==========================================================
# AI Model Reference Data
# ==========================================================

AI_MODELS = [

    {
        "Model_Code":"AI001",
        "Model_Name":"Disease Risk Prediction",
        "Algorithm":"Random Forest",
        "Category":"Classification",
        "Version":"1.0",
        "Accuracy":"94.30%",
        "Status":"Production",
        "Description":"Predicts future disease risk."
    },

    {
        "Model_Code":"AI002",
        "Model_Name":"Hospital Readmission Prediction",
        "Algorithm":"XGBoost",
        "Category":"Classification",
        "Version":"1.0",
        "Accuracy":"92.80%",
        "Status":"Production",
        "Description":"Predicts readmission probability."
    },

    {
        "Model_Code":"AI003",
        "Model_Name":"ICU Mortality Prediction",
        "Algorithm":"LightGBM",
        "Category":"Classification",
        "Version":"1.0",
        "Accuracy":"95.10%",
        "Status":"Production",
        "Description":"Predicts ICU mortality risk."
    },

    {
        "Model_Code":"AI004",
        "Model_Name":"Length of Stay Prediction",
        "Algorithm":"CatBoost",
        "Category":"Regression",
        "Version":"1.0",
        "Accuracy":"91.20%",
        "Status":"Production",
        "Description":"Predicts hospital stay duration."
    },

    {
        "Model_Code":"AI005",
        "Model_Name":"Sepsis Early Detection",
        "Algorithm":"XGBoost",
        "Category":"Classification",
        "Version":"1.0",
        "Accuracy":"96.00%",
        "Status":"Production",
        "Description":"Early warning for sepsis."
    },

    {
        "Model_Code":"AI006",
        "Model_Name":"Diabetes Prediction",
        "Algorithm":"Logistic Regression",
        "Category":"Classification",
        "Version":"1.0",
        "Accuracy":"90.60%",
        "Status":"Production",
        "Description":"Predicts diabetes occurrence."
    },

    {
        "Model_Code":"AI007",
        "Model_Name":"Heart Disease Prediction",
        "Algorithm":"Random Forest",
        "Category":"Classification",
        "Version":"1.0",
        "Accuracy":"93.40%",
        "Status":"Production",
        "Description":"Predicts cardiovascular disease."
    },

    {
        "Model_Code":"AI008",
        "Model_Name":"Kidney Disease Prediction",
        "Algorithm":"Gradient Boosting",
        "Category":"Classification",
        "Version":"1.0",
        "Accuracy":"94.10%",
        "Status":"Production",
        "Description":"Predicts chronic kidney disease."
    },

    {
        "Model_Code":"AI009",
        "Model_Name":"Patient Health Score",
        "Algorithm":"Ensemble Learning",
        "Category":"Scoring",
        "Version":"1.0",
        "Accuracy":"95.70%",
        "Status":"Production",
        "Description":"Generates overall patient health score."
    },

    {
        "Model_Code":"AI010",
        "Model_Name":"Clinical Decision Support",
        "Algorithm":"Rule Based + ML",
        "Category":"Recommendation",
        "Version":"1.0",
        "Accuracy":"97.20%",
        "Status":"Production",
        "Description":"Generates AI clinical recommendations."
    }

]


# ==========================================================
# Generate Dataset
# ==========================================================

def generate_reference_ai_models():

    dataframe = pd.DataFrame(
        AI_MODELS
    )

    path = os.path.join(
        config.REFERENCE_DIR,
        "reference_ai_models.csv"
    )

    dataframe.to_csv(
        path,
        index=False
    )

    print(
        "Created reference_ai_models.csv" 
    )

    print(
        f"Generated {len(dataframe)} AI model references."
    )


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    generate_reference_ai_models()