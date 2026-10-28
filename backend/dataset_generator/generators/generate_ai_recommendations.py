"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_ai_recommendations.py

Purpose :
Generate AI clinical recommendations.

Input:
ai_predictions.csv
patients.csv

Output:
ai_recommendations.csv

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
# Files
# ==========================================================


PREDICTION_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "ai_predictions.csv"
)


PATIENT_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "patients.csv"
)



# ==========================================================
# Recommendation Templates
# ==========================================================


RECOMMENDATIONS = [

    "Regular monitoring of vital signs recommended",

    "Schedule follow-up consultation",

    "Review medication adherence",

    "Perform additional laboratory investigations",

    "Lifestyle modification advised",

    "Consider specialist consultation",

    "Monitor patient closely for deterioration",

    "Continue current treatment plan"

]



# ==========================================================
# Generate AI Recommendations
# ==========================================================


def generate_ai_recommendations():


    show_progress(
        "Generating AI Recommendations Dataset"
    )



    predictions = pd.read_csv(
        PREDICTION_FILE
    )


    patients = pd.read_csv(
        PATIENT_FILE
    )



    records = []

    prediction_index = np.random.randint(
        0,
        len(predictions),
        config.NUM_AI_RECOMMENDATIONS
    )




    for i in range(
        config.NUM_AI_RECOMMENDATIONS
    ):



        prediction = predictions.iloc[
            prediction_index[i]
        ]




        risk = prediction[
            "Prediction_Result"
        ]



        priority = (

            "High"

            if risk == "High Risk"

            else

            "Medium"

            if risk == "Medium Risk"

            else

            "Low"

        )



        record = {



            "Recommendation_ID":
                generate_uuid(),


            "Patient_ID":
                prediction["Patient_ID"],


            "AI_Prediction_ID":
                prediction["AI_Prediction_ID"],


            "Recommendation_Type":
                random.choice(
                    [
                    "Preventive Care",
                    "Treatment Support",
                    "Risk Management",
                    "Monitoring"
                    ]
                ),


            "Recommendation_Text":
                random.choice(
                    RECOMMENDATIONS
                ),


            "Priority_Level":
                priority,


            "AI_Confidence":

                prediction[
                    "Confidence_Score"
                ],


            "Doctor_Review_Status":
                random.choice(
                    [
                    "Pending",
                    "Reviewed",
                    "Approved"
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
                f"{i+1} AI recommendations generated"
            )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "ai_recommendations.csv"
    )



    print(
        f"Generated {len(dataframe)} AI recommendations"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_ai_recommendations()