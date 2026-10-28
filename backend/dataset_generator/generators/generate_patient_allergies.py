"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_patient_allergies.py

Purpose :
Generate ground-truth based patient allergy records.

Input:
patients.csv

Output:
patient_allergies.csv

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import random
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
# Load Patient Data
# ==========================================================


PATIENT_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "patients.csv"
)



# ==========================================================
# Ground Truth Allergies
# ==========================================================


ALLERGIES = [

    {
        "Allergen":"Penicillin",
        "Category":"Medication",
        "Severity":"High"
    },

    {
        "Allergen":"Aspirin",
        "Category":"Medication",
        "Severity":"Medium"
    },

    {
        "Allergen":"Peanuts",
        "Category":"Food",
        "Severity":"High"
    },

    {
        "Allergen":"Milk",
        "Category":"Food",
        "Severity":"Medium"
    },

    {
        "Allergen":"Eggs",
        "Category":"Food",
        "Severity":"Medium"
    },

    {
        "Allergen":"Dust",
        "Category":"Environmental",
        "Severity":"Low"
    },

    {
        "Allergen":"Pollen",
        "Category":"Environmental",
        "Severity":"Low"
    },

    {
        "Allergen":"Latex",
        "Category":"Material",
        "Severity":"Medium"
    }

]



# ==========================================================
# Generate Allergies
# ==========================================================


def generate_patient_allergies():


    show_progress(
        "Generating Patient Allergy Dataset"
    )


    patients = pd.read_csv(
        PATIENT_FILE
    )


    records = []



    for _, patient in patients.iterrows():


        # Around 20% patients have allergies

        if random.random() < 0.20:


            allergy_count = random.randint(
                1,
                2
            )


            selected_allergies = random.sample(
                ALLERGIES,
                allergy_count
            )



            for allergy in selected_allergies:


                record = {


                    "Allergy_ID":
                        generate_uuid(),


                    "Patient_ID":
                        patient["Patient_ID"],


                    "Allergen":
                        allergy["Allergen"],


                    "Category":
                        allergy["Category"],


                    "Severity":
                        allergy["Severity"],


                    "Reaction":
                        random.choice(
                            [
                            "Rash",
                            "Swelling",
                            "Breathing Difficulty",
                            "Itching",
                            "Nausea"
                            ]
                        ),


                    "Diagnosis_Date":
                        patient["Date_of_Birth"],


                    "Status":
                        "Active"

                }


                records.append(
                    record
                )



    dataframe = pd.DataFrame(
        records
    )


    save_dataframe(
        dataframe,
        "patient_allergies.csv"
    )


    print(
        f"Generated {len(dataframe)} allergy records"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_patient_allergies()