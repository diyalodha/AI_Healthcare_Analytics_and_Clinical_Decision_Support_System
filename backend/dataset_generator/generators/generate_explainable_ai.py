"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_explainable_ai.py

Purpose :
Generate Explainable AI records.

Input:
ai_predictions.csv

Output:
explainable_ai.csv

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import random
import numpy as np
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


from utils import (
    generate_uuid,
    save_dataframe,
    show_progress
)



# ==========================================================
# File
# ==========================================================


PREDICTION_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "ai_predictions.csv"
)



# ==========================================================
# Explainable AI Features
# ==========================================================


FEATURES = [

    "Age",
    "Blood Pressure",
    "Heart Rate",
    "Blood Glucose Level",
    "Kidney Function",
    "BMI",
    "Previous Diagnosis",
    "Medication History",
    "Hospital Admission History"

]



# ==========================================================
# Generate XAI Records
# ==========================================================


def generate_explainable_ai():


    show_progress(
        "Generating Explainable AI Dataset"
    )



    predictions = pd.read_csv(
        PREDICTION_FILE
    )



    records = []

    prediction_index = np.random.randint(
        0,
        len(predictions),
        config.NUM_EXPLAINABLE_AI
    )


    for i in range(
        config.NUM_EXPLAINABLE_AI
    ):



        prediction = predictions.iloc[
            prediction_index[i]
        ]


        feature = random.choice(
            FEATURES
        )



        contribution = round(
            random.uniform(
                0.01,
                0.50
            ),
            3
        )



        impact = (

            "High Impact"

            if contribution > 0.30

            else

            "Medium Impact"

            if contribution > 0.15

            else

            "Low Impact"

        )



        record = {



            "Explainability_ID":
                generate_uuid(),


            "AI_Prediction_ID":
                prediction[
                    "AI_Prediction_ID"
                ],


            "Patient_ID":
                prediction[
                    "Patient_ID"
                ],


            "Feature_Name":
                feature,


            "Feature_Value":

                random.choice(
                    [
                    "Normal",
                    "Elevated",
                    "Abnormal",
                    "Critical"
                    ]
                ),


            "Contribution_Score":
                contribution,


            "Impact_Level":
                impact,


            "Explanation":

                (
                feature
                +
                " contributed to the prediction "
                "based on clinical patterns."
                ),


            "Model_Interpretation_Method":

                random.choice(
                    [
                    "SHAP",
                    "LIME",
                    "Feature Importance",
                    "Rule Based Explanation"
                    ]
                ),


            "Generated_Date":
                prediction[
                    "Prediction_Date"
                ]



        }



        records.append(
            record
        )



        if (i + 1) % 50000 == 0:

            print(
                f"{i+1} explainable AI records generated"
            )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "explainable_ai.csv"
    )



    print(
        f"Generated {len(dataframe)} explainable AI records"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_explainable_ai()